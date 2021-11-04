import os

items_pickup_eligibility_from_env = os.getenv('ITEMS_PICKUP_ELIGIBILITY', "") # or "Z14W,Z14X"
PICKUP_ELIGIBILITY = items_pickup_eligibility_from_env.split(",")

items_pickup_availability_from_env = os.getenv('ITEMS_PICKUP_AVAILABILITY', "") # or "Z14W,Z14X,MK1A3LL/A,MK193LL/A"
PICKUP_AVAILABILITY = items_pickup_availability_from_env.split(",")

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', "")
TELEGRAM_CHATID = os.getenv('TELEGRAM_CHATID', "")

ZIP_CODE = os.getenv('ZIP', "") # or '07029'
