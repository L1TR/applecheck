# AppleStore PickUp Checker Telegram Bot
Build: <code>docker build -t applecheck .</code>

Save to the file: <code>docker save applecheck > applecheck.tar</code>

<h2>Setup</h2>

All configuration variables are stored in the src/common/config.py
1. - Provide TELEGRAM_TOKEN as ENV variables or change defaults in dockerfile

2. Change ENV "ITEMS_PICKUP_AVAILABILITY" to check changes in pickup availability

Tested on MacOS and Synology DiskStation
