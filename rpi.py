import RPi.GPIO as gpio

from logger import Logger


class RPIGpio():

    PIN = 14
    STATE = True

    def __init__(self):
        self.logger = Logger.getLogger()

    def setup(self):
        self.logger.debug("Initializing RPI library")
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.PIN, gpio.OUT)
        gpio.output(self.PIN, self.STATE)

    def toggle(self):
        self.STATE = not self.STATE
        gpio.output(self.PIN, self.STATE)

    def get_state(self):
        return not self.STATE