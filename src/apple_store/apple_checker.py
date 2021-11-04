import requests
from collections import defaultdict
from common.consts import APPLE_STORE_FULFILLMENT_URL
from common.config import ZIP_CODE, PICKUP_ELIGIBILITY, PICKUP_AVAILABILITY

class AppleChecker(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            }
        self.url = APPLE_STORE_FULFILLMENT_URL

    def checkState(self):
        available_for_pickup = defaultdict(list)
        eligible_for_pickup = defaultdict(list)
        params = {'location': ZIP_CODE}
        all_items = list(set(PICKUP_ELIGIBILITY + PICKUP_AVAILABILITY))
        for i, item in enumerate(all_items):
            params[f'parts.{i}'] = item

        response = requests.get(self.url, params=params)
        try:
            stores = response.json()['body']['content']['pickupMessage']['stores']
            for store in stores:
                for item in PICKUP_ELIGIBILITY:
                    part_availability = store['partsAvailability'].get(item, {})
                    if part_availability and part_availability['pickupDisplay'] != 'ineligible':
                        eligible_for_pickup[item].append([store['storeName']])
                for item in PICKUP_AVAILABILITY:
                    part_availability = store['partsAvailability'].get(item, {})
                    if part_availability and part_availability['pickupDisplay'] not in ['ineligible', 'unavailable']:
                        available_for_pickup[item].append([store['storeName']])
        except:
            # Possible in stock
            print("Error. Response: ", response.text)
            return None, None
        return available_for_pickup, eligible_for_pickup
