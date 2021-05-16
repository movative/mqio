import time
from time import sleep
import RPi.GPIO as GPIO
import logging as lg
from enum import Enum
import click


logger: lg.Logger = lg.getLogger(__name__)


class SingleColor:

    def __init__(self, pin: int = 8):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.setwarnings(False)
        self.pin = pin

    def blink(self, interval: float):
        GPIO.output(self.pin, True)
        time.sleep(interval)
        GPIO.output(self.pin, False)
        time.sleep(interval)

    def loop(self):
        GPIO.PWM(self.pin, 100)


class TriColor:

    def __init__(self, red_pin: int = 17, green_pin: int = 18, blue_pin: int = 27, freq: int = 100):

        logger.info(f"Initialized LED Type RGB: {red_pin}, {green_pin}, {blue_pin}")

        # Set GPIO to Broadcom system and set pins to output mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)

        # Setup all the LED colors with an initial and duty cycle of 0 which is off
        self.RED = GPIO.PWM(red_pin, freq)
        self.RED.start(0)
        self.GREEN = GPIO.PWM(green_pin, freq)
        self.GREEN.start(0)
        self.BLUE = GPIO.PWM(blue_pin, freq)
        self.BLUE.start(0)

    def color(self, red, green, blue, on_time):
        self.RED.ChangeDutyCycle(red)
        self.GREEN.ChangeDutyCycle(green)
        self.BLUE.ChangeDutyCycle(blue)
        sleep(on_time)
        self.RED.ChangeDutyCycle(0)
        self.GREEN.ChangeDutyCycle(0)
        self.BLUE.ChangeDutyCycle(0)

    def loop(self):
        for x in range(0, 2):
            for y in range(0, 2):
                for z in range(0, 2):
                    logger.debug(x, y, z)
                    for i in range(0, 101):
                        self.color((x * i), (y * i), (z * i), .02)


class LED(Enum):
    SingleColor = 1
    TriColor = 2


@click.command()
def led(device: LED):
    try:
        logger.info("Light It Up! Press CTRL + C to quit.\n")
        if device == LED.SingleColor:
            sc: SingleColor = SingleColor()
            while True:
                sc.loop()
        elif device == LED.TriColor:
            tc: TriColor = TriColor()
            while True:
                tc.loop()
    except KeyboardInterrupt:
        logger.info("Interrupted by Keyboard (CTRL+C)")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    led()
