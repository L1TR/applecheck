from collections import defaultdict
from apple_store.apple_checker import AppleChecker
from common.consts import PRODUCT_CODE_TO_NAME
import threading


class Runner(object):
    def __init__(self, resultHandler, productsToCheck):
        self.telegramHandler = resultHandler
        self.appleChecker = AppleChecker()
        self.timesChecked = 0
        self.zip = None
        self.runningEvent = None
        self.productsToCheck = productsToCheck
        self.availabilityStates = { k:0 for k in productsToCheck}

    def checkState(self):
        """
        Checks state of the items in the Apple store
        """
        print("Checking --- START")
        if not self.zip:
            self.telegramHandler("Enter valid zip code to start")
        available = self.appleChecker.checkState(self.zip, toCheck=self.productsToCheck)
        result = []
        if available is None:
            print('Error')
            result.append('Something wrong with Apple store cheker')
        else:
            for k in self.productsToCheck:
                v = available.get(k, [])
                l = len(v)
                if self.availabilityStates.get(k, 0) != l:
                    product_name = PRODUCT_CODE_TO_NAME.get(k, k)
                    if l > 1:
                        result.append(f"{product_name} is available in {l} stores")
                    elif l == 1:
                        result.append(f"{product_name} is available in {v[0]}")
                    else:
                        result.append(f"{product_name} is not available")
        self.availabilityStates = {k:len(available.get(k, [])) for k in self.productsToCheck}
        if result:
            self.telegramHandler('\n'.join(result))
        self.timesChecked += 1
        print("Checking --- END")

    def runCheck(self, zip):
        self.zip = zip
        self.telegramHandler(f"Starting Apple store checker for ZIP code '{self.zip}'")
        def run(run_stop):
            if not run_stop.is_set():
                self.checkState()
                threading.Timer(60, run, [run_stop]).start()
        self.runningEvent = threading.Event()
        run(self.runningEvent)
    
    def stopCheck(self):
        if self.runningEvent:
            self.runningEvent.set()
        self.timesChecked = 0


def main():
    runner = Runner()
    runner.runCheck()


if __name__ == "__main__":
    main()
