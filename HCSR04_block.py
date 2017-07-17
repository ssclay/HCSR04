from nio.block.base import Block
from nio.properties import VersionProperty
import RPi.GPIO as GPIO
import os, signal
import time

class HCSR04(Block):

    version = VersionProperty('0.1.0')
    #GPIO Numbers
    TRIG = 23
    ECHO = 24

    def __init__(self, TRIG, ECHO):
        self.TRIG = TRIG
        self.ECHO = ECHO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)


    def process_signals(self, signals):
        for signal in signals:
            GPIO.output(self.TRIG, False)
            time.sleep(0.5) #Time between readings
            #TRIGGER
            GPIO.output(self.TRIG, True)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, False)

            while GPIO.input(self.ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(self.ECHO) == 1:
                pulse_end = time.time()

            pulse_length = pulse_end - pulse_start
            #17150 = 1/2 speed of sound due to two trips of the sound
            distance = pulse_length * 17150
            distance = round(distance, 2) #in cm

        self.notify_signals(signals)
