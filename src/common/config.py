import os

items_pickup_availability_from_env = os.getenv('ITEMS_PICKUP_AVAILABILITY', "Z14W,Z14X,MK1A3LL/A,MK1H3LL/A,Z14Z,MK193LL/A")
PICKUP_AVAILABILITY = items_pickup_availability_from_env.split(",")

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', "")
