import RPi.GPIO as gpio

class RPIGpio():

    PIN = 14
    STATE = True

    def setup(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.PIN, gpio.OUT)
        gpio.output(self.PIN, self.STATE)

    def toggle(self):
        self.STATE = not self.STATE
        gpio.output(self.PIN, self.STATE)