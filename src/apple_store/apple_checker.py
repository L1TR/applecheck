import requests
from collections import defaultdict
from common.consts import APPLE_STORE_FULFILLMENT_URL
from common.helpers import translated_names

class AppleChecker(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            }
        self.url = APPLE_STORE_FULFILLMENT_URL

    # @translated_names
    def checkState(self, zipCode, toCheck):
        available_for_pickup = defaultdict(list)
        params = {'location': zipCode}
        for i, item in enumerate(toCheck):
            params[f'parts.{i}'] = item

        try:
            response = requests.get(self.url, params=params)
            stores = response.json()['body']['content']['pickupMessage']['stores']
            for store in stores:
                for item in toCheck:
                    part_availability = store['partsAvailability'].get(item, {})
                    if part_availability and part_availability['pickupDisplay'] not in ['ineligible', 'unavailable']:
                        available_for_pickup[item].append([store['storeName']])
        except:
            # Possible in stock
            print("Error. Response: ", response.text)
            return None
        return available_for_pickup
