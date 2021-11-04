import sched, time
from collections import defaultdict
from typing import DefaultDict
from common.telegram_sender import TelegramSender
from apple_store.apple_checker import AppleChecker
from common.config import ZIP_CODE

IS_DEBUG = False  # __debug__ doesn't work as expected in Docker


class Runner(object):
    def __init__(self):
        self.logger = TelegramSender()
        self.appleChecker = AppleChecker()
        self.availabilityStates = defaultdict(int)
        self.eligibilityStates = defaultdict(int)

    def checkState(self):
        """
        Checks state of the items in the Apple store
        """
        print("Checking --- START")
        available, eligible = self.appleChecker.checkState()
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
        if eligible:
            for k, v in eligible.items():
                l = v.len()
                if self.eligibilityStates[k] != l:
                    self.eligibilityStates[k] = l
                    if l > 1:
                        result.append(f"{k} eligible in {l} stores")
                    else:
                        result.append(f"{k} eligible in {v[0]}")
        if result:
            self.logger.send('\n'.join(result))
        print("Checking --- END")

    def runCheck(self):
        self.checkState()


def main():
    runner = Runner()
    if IS_DEBUG:
        runner.runCheck()
    else:
        scheduler = sched.scheduler(time.time, time.sleep)
        runner.logger.send(f"Starting Apple store checker for ZIP code '{ZIP_CODE}'")
        def run(sc):
            runner.runCheck()
            scheduler.enter(60, 1, run, (sc,))

        scheduler.enter(2, 1, run, (scheduler,))
        scheduler.run()


if __name__ == "__main__":
    main()
