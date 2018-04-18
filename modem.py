from typing import List
from curses import ascii

import serial
import time
import re

from logger import Logger


class ATModem:

    sms = re.compile(r"CMGL:\s\d,\".+\",\"(.+)\",\"\",\"[0-9:+ /,]+\"\n\n(.*),\d,\d\n\n")

    def __init__(self):
        self.modem = serial.Serial("/dev/ttyACM0", baudrate=115200)
        self.logger = Logger.getLogger()

    def close(self):
        if self.modem.is_open:
            self.modem.close()

    def sendSMS(self, number: str, data: str):

        self.logger.debug("Sending SMS messsage >{}< to {}".format(data, number))

        self.logger.debug("AT+CMGF")
        self.modem.write(b"AT+CMGF=1\r")
        time.sleep(0.5)
        self.logger.debug(self.read_all())

        self.logger.debug("AT+CSCS")
        self.modem.write(b"AT+CSCS=\"GSM\"\r")
        time.sleep(0.5)
        self.logger.debug(self.read_all())

        self.logger.debug("AT+CMGS")
        self.modem.write("AT+CMGS=\"{}\"\r".format(number).encode("ascii"))
        time.sleep(0.5)
        self.modem.write(data.encode("ascii"))
        time.sleep(0.5)
        self.modem.write(ascii.ctrl('z').encode("ascii"))

        self.logger.debug(self.read_all())

        self.logger.debug("Message sent")

    def __check(self, modem):
        self.logger.debug("Checking messages")
        time.sleep(0.5)
        ret = modem.read_all().decode("ascii")
        if "ERROR" in ret:
            self.logger.error("Sending failed, modem insane")
            return True
        return False

    def wait_for_all(self):
        self.logger.debug("Waiting for data from modem")
        current = self.modem.inWaiting()
        previous = current
        counter = 0
        while counter < 5:
            self.logger.debug("loop iteration")
            if current == previous:
                time.sleep(0.5)
                current = self.modem.inWaiting()
                previous = current
                counter += 1

    def read_all(self):
        self.wait_for_all()
        return self.modem.read_all().decode("utf-8")

    def listSMSMessages(self) -> List[tuple]:
        self.modem.write(b"AT+CMGL\r")
        lines = self.read_all().split("\r\n")
        ret = []
        for i in range(0, len(lines)):
            if "CMGL: " in lines[i]:
                ret.append({
                    "id": int(lines[i].split(",")[0].replace(" ", "").replace("+CMGL:", "")),
                    "number": lines[i].split(",")[2].replace("\"", ""),
                    "message": lines[i + 1].replace(",0,0", "").replace("\n", "<LF>")
                })
        return ret
