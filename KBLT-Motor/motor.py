from logger import LOGGER
from periphery import GPIO
import time


class Motor:
    def __init__(self, pulse_pin, direction_pin):
        self.dead_duration = 1

        self.pulse_pin = GPIO(pulse_pin, "out")
        self.direction_pin = GPIO(direction_pin, "out")
        LOGGER.debug("Motor initialized")

    def turn_motor(self, pulse_duration):
        LOGGER.debug("Start turning motor")
        self.pulse_pin.write(True)
        time.sleep(pulse_duration)

    def hold_motor(self, hold_duration):
        LOGGER.debug("Stop turning motor")
        self.pulse_pin.write(False)
        time.sleep(hold_duration)

    def turn_off(self):
        self.pulse_pin.write(False)
        self.pulse_pin.close()
        self.direction_pin.close()
        LOGGER.debug("Motor turned OFF")
