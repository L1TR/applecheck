# Apple store pickup availability informer Telegram Bot
Build: <code>docker build -t applecheck .</code>

Export to the file: <code>docker save applecheck > applecheck.tar</code>

<h2>Setup</h2>

All configuration variables are stored in the src/common/config.py
1. Provide TELEGRAM_TOKEN in ENVs or change defaults in dockerfile

2. (optional) Change ENV "ITEMS_PICKUP_AVAILABILITY"

Tested on MacOS and Synology DiskStation

Docker page: https://hub.docker.com/r/l1tr/applepickup
