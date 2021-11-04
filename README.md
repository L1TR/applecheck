# ps5instore
Build: <code>docker build -t applecheck .</code>

Save to the file: <code>docker save applecheck > applecheck.tar</code>

<h2>Setup</h2>

All configuration variables are stored in the src/common/config.py
1. (required) <b>Telegram</b> bot to receive updates
- Register your own bot: https://core.telegram.org/bots#6-botfather
- Go to the <code>htt<span>ps://api.telegram.org/bot{your_token}/getUpdates</code> to get chat id
- Provide TELEGRAM_TOKEN and TELEGRAM_CHATID as ENV variables or change defaults in dockerfile

2. Change ENV "ZIP" with your zip code

3. Change ENV "ITEMS_PICKUP_ELIGIBILITY" and "ITEMS_PICKUP_AVAILABILITY" to check changes in pickup eligibility and availability


Tested on MacOS and Synology DiskStation
