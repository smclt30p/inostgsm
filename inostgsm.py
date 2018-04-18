import sys

import time

from modem import ATModem
from rpi import RPIGpio

pi = RPIGpio()
pi.setup()
modem = ATModem()

def main():

    high = 0

    while True:
        messages = modem.listSMSMessages()
        if len(messages) == 0:
            print("modem crapped out, skipping")
            continue

        if high == 0:
            print("setting initial")
            high = highest_id(messages)
            continue

        if highest_id(messages) > high:
            high = highest_id(messages)
            trigger_event(messages, high)

        print("checked {} msgs".format(len(messages)))
        time.sleep(5)


def highest_id(msgs):
    h = 0
    for msg in msgs:
        if (msg["id"] > h):
            h = msg["id"]
    return h


def trigger_event(messages, index):
    pi.toggle()

if __name__ == "__main__":
    main()
