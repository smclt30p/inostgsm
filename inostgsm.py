import sys

import time

from modem import ATModem
from rpi import RPIGpio


def main():

    pi = RPIGpio()
    pi.setup()

    while True:
        time.sleep(0.1)
        pi.toggle()
        time.sleep(0.1)
        pi.toggle()

    modem = ATModem()
    print("sending test msg")
    modem.sendSMS("+38766064783", "This is a test message");

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


def highest_id(msgs):
    h = 0
    for msg in msgs:
        if (msg["id"] > h):
            h = msg["id"]
    return h


def trigger_event(messages, index):
    print("event triggered")
    print(message)

if __name__ == "__main__":
    main()
