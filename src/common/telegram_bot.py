import requests
import re
from common.config import TELEGRAM_TOKEN
from common.runner import Runner
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class TelegramBot(object):
    def __init__(self, chatId):
        self.token = TELEGRAM_TOKEN
        self.chatId = str(chatId)
        self.runner = Runner(resultHandler=self.send)
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
                context.bot.send_message(chat_id=chat_id, text="""Hi, 
                1. To start send '/run {zip code}
                2. To stop - just send /stop
                3. To check iteration id - /ping""")

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

    def ping(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.bots:
            bot = self.bots[chat_id]
            context.bot.send_message(chat_id=chat_id, text=f"Completed iterations: {bot.runner.timesChecked}")


def run():
    farm = TelegramFarm()
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", farm.spawnBot))
    dp.add_handler(CommandHandler("run", farm.run))
    dp.add_handler(CommandHandler("stop", farm.stop))
    dp.add_handler(CommandHandler("ping", farm.ping))
    updater.start_polling()
    updater.idle()
