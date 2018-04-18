import sys

import time

from modem import ATModem
from rpi import RPIGpio


VERSION = "1.0"

class InostGSM():

    __msgHigh = 0

    def __init__(self):
        print("Starting InostGSM version {}".format(VERSION))
        print("Initializing GPIO library")
        self.pi = RPIGpio()
        print("Initializing AT library")
        self.modem = ATModem()
        pass

    def highest_id(self, msgs):
        h = 0
        for msg in msgs:
            if (msg["id"] > h):
                h = msg["id"]
        return h

    def run(self):
        while True:
            msgs = self.modem.listSMSMessages()
            if len(msgs) == 0:
                print("Modem is insane, skipping iteration")
                continue
            if self.__msgHigh == 0:
                print("Setting iniital mainloop ctr")
                self.__msgHigh = self.highest_id(msgs)
                continue
            if self.highest_id(msgs) > self.__msgHigh:
                self.__msgHigh = self.highest_id(msgs)
                self.defevent_trigger(msgs)

            print("mainloop iteration, checked {} SMS msgs".format(len(msgs)))
            time.sleep(5)

    def defevent_trigger(self, messages):
        pass

def main():
    gsm = InostGSM()
    gsm.run()

if __name__ == "__main__":
    main()
