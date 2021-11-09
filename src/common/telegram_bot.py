import requests
import re
from common.config import TELEGRAM_TOKEN, PICKUP_AVAILABILITY
from common.runner import Runner
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from common.consts import PRODUCT_CODE_TO_NAME


class TelegramBot(object):
    def __init__(self, chatId):
        self.token = TELEGRAM_TOKEN
        self.productsToCheck = PICKUP_AVAILABILITY
        self.chatId = str(chatId)
        self.runner = Runner(resultHandler=self.send, productsToCheck=self.productsToCheck)
        self.running = False

    def send(self, log):
        send_url = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chatId + '&parse_mode=Markdown&text=' + log
        response = requests.get(send_url)
        return response.json()

    def start(self, zip):
        self.running = True
        self.runner.runCheck(zip=zip)
    
    def stop(self):
        self.runner.stopCheck()
        self.running = False


class TelegramFarm(object):
    def __init__(self):
        self.bots = {}
    
    def spawnBot(self, update, context, silent=False):
        chat_id = update.effective_chat.id
        print('Start chat with', chat_id)
        if chat_id in self.bots:
            context.bot.send_message(chat_id=chat_id, text="If you want to stop checking items in the store - send /stop")
        else:
            self.bots[chat_id] = TelegramBot(chatId=chat_id)
            if not silent:
                context.bot.send_message(chat_id=chat_id, text="""Hello,

                1. To start send '/run {zip code}
                2. To stop - just send /stop
                3. To check iteration id - /ping
                4. To get current state for all products - /info
                5. To add product - /add {product code} (for example, /add MK193LL/A)
                6. Ro remove product - /remove {product code}""")

    def run(self, update, context):
        chat_id = update.effective_chat.id
        print('Run checking for', chat_id)
        if chat_id not in self.bots:
            self.spawnBot(update, context, silent=True)
        bot = self.bots[chat_id]
        if bot.running:
            context.bot.send_message(chat_id=chat_id, text="You already have running process. Please stop it by sending command /stop")
        else:
            try:
                postal_code = re.search(r'.*(\d{5}(\-\d{4})?)$', update.message.text)
                zip = postal_code.groups()[0]
                bot.start(zip)
            except Exception as ex:
                print(ex)

    def stop(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            bot.stop()
            context.bot.send_message(chat_id=chat_id, text=f"Stopped for zip '{bot.runner.zip}'")

    def ping(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            context.bot.send_message(chat_id=chat_id, text=f"Completed checks: {bot.runner.timesChecked}")

    def info(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            if bot.running:
                res = '\n'.join(["{} available in {} stores".format(PRODUCT_CODE_TO_NAME.get(p, p), bot.runner.availabilityStates.get(p, 0)) for p in bot.productsToCheck])
                context.bot.send_message(chat_id=chat_id, text=f"Current state for products:\n Zip code: {bot.runner.zip}\n{res}")
            else:
                context.bot.send_message(chat_id=chat_id, text=f"Doing nothing. Send /run zip to start")

    def add(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            item = update.message.text.split(' ')[1]
            if item not in bot.productsToCheck:
                bot.productsToCheck.append(item)
                context.bot.send_message(chat_id=chat_id, text=f"Added product code '{item}'")
            else:
                context.bot.send_message(chat_id=chat_id, text=f"This product already in your list")

    def remove(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            self.remove_product(bot, chat_id, context, update.message.text)


    def remove_product(self, bot, chatId, context, text):
        parts = text.split(' ')
        item = parts[1] if parts and len(parts) > 1 else None
        if item in bot.productsToCheck:
            bot.productsToCheck.remove(item)
            context.bot.send_message(chat_id=chatId, text=f"Removed product code '{item}'")
        elif not item:
            remove_buttons = []
            for code in bot.productsToCheck:
                remove_buttons.append([telegram.InlineKeyboardButton(
                    text=PRODUCT_CODE_TO_NAME.get(code, code),
                    callback_data=f"/remove {code}"
                )])
            context.bot.send_message(
                chat_id=chatId, 
                text=f"Click on product you want to remove", 
                reply_markup=telegram.InlineKeyboardMarkup(remove_buttons)
            )
        else:
            context.bot.send_message(chat_id=chatId, text=f"You have no this product code in your config")


    def codes(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            if bot.running:
                codes = '\n'.join(bot.productsToCheck)
                context.bot.send_message(chat_id=chat_id, text=f"Product codes:\n {codes}")
            else:
                context.bot.send_message(chat_id=chat_id, text=f"Doing nothing. Send /run zip to start")

    def callback_handler(self, update, context):
        query_data = update.callback_query.data
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            if query_data.startswith("/remove"):
                self.remove_product(bot, chat_id, context, query_data)



def run():
    farm = TelegramFarm()
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", farm.spawnBot))
    dp.add_handler(CommandHandler("run", farm.run))
    dp.add_handler(CommandHandler("stop", farm.stop))
    dp.add_handler(CommandHandler("ping", farm.ping))
    dp.add_handler(CommandHandler("add", farm.add))
    dp.add_handler(CommandHandler("remove", farm.remove))
    dp.add_handler(CommandHandler("info", farm.info))
    dp.add_handler(CommandHandler("codes", farm.codes))
    dp.add_handler(CallbackQueryHandler(farm.callback_handler))
    updater.start_polling()
    updater.idle()
