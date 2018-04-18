import time

from modem import ATModem
from rpi import RPIGpio
from logger import Logger

VERSION = "1.0"

class InostGSM():

    __msgHigh = 0

    def __init__(self):
        print("Starting InostGSM version {}".format(VERSION))
        self.rootLogger = Logger.getLogger()
        self.rootLogger.debug("Initializing GPIO library")
        self.pi = RPIGpio()
        self.rootLogger.debug("Initializing AT library")
        self.modem = ATModem()

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
                self.rootLogger.debug("Modem is insane, skipping iteration")
                continue
            if self.__msgHigh == 0:
                self.rootLogger.debug("Setting iniital mainloop ctr")
                self.__msgHigh = self.highest_id(msgs)
                continue
            if self.highest_id(msgs) > self.__msgHigh:
                self.__msgHigh = self.highest_id(msgs)
                self.defevent_trigger(msgs, self.__msgHigh - 1)

            self.rootLogger.debug("mainloop iteration, checked {} SMS msgs".format(len(msgs)))
            time.sleep(5)

    def defevent_trigger(self, messages, index):
        self.rootLogger.debug("Triggered SMS event")
        self.rootLogger.debug(
            "message: {}, id: {}, number: {}".format(
                messages[index]["message"],
                messages[index]["id"],
                messages[index]["number"]
            )
        )
        pass

def main():
    gsm = InostGSM()
    gsm.run()

if __name__ == "__main__":
    main()
