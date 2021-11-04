import sched, time
from collections import defaultdict
from apple_store.apple_checker import AppleChecker
from common.config import PICKUP_AVAILABILITY
import threading


class Runner(object):
    def __init__(self, resultHandler):
        self.telegramHandler = resultHandler
        self.appleChecker = AppleChecker()
        self.availabilityStates = defaultdict(int)
        self.scheduler = None
        self.timesChecked = 0
        self.zip = None
        self.backgroundThread = None
        self.eventId = None

    def checkState(self):
        """
        Checks state of the items in the Apple store
        """
        print("Checking --- START")
        if not self.zip:
            self.telegramHandler("Enter valid zip code to start")
        available = self.appleChecker.checkState(self.zip, toCheck=PICKUP_AVAILABILITY)
        result = []
        if available is None:
            print('Error')
            result.append('Something wrong with Apple store cheker')
        if available:
            for k, v in available.items():
                l = len(v)
                if self.availabilityStates[k] != l:
                    self.availabilityStates[k] = l
                    if l > 1:
                        result.append(f"{k} available in {l} stores")
                    else:
                        result.append(f"{k} available in {v[0]}")
        if result:
            self.telegramHandler('\n'.join(result))
        self.timesChecked += 1
        print("Checking --- END")

    def runWithScheduler(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        def run(sc):
            self.checkState()
            self.eventId = self.scheduler.enter(60, 1, run, (sc,))

        self.scheduler.enter(2, 1, run, (self.scheduler,))
        self.scheduler.run()

    def runCheck(self, zip):
        self.zip = zip
        self.telegramHandler(f"Starting Apple store checker for ZIP code '{self.zip}'")
        self.backgroundThread = threading.Thread(name='background', target=self.runWithScheduler)
        self.backgroundThread.start()
    
    def stopCheck(self):
        if self.eventId:
            self.scheduler.cancel(self.eventId)


def main():
    runner = Runner()
    runner.runCheck()


if __name__ == "__main__":
    main()
