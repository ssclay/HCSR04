from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty
from nio.signal.base import Signal
import RPi.GPIO as GPIO
import os, signal
import time

class HCSR04(Block):

    version = VersionProperty('0.1.0')
    trig = IntProperty(title = "Trigger GPIO", default = 0)
    echo = IntProperty(title = "Echo GPIO", default = 0)
    pulse_start = None
    pulse_end = None

    def configure(self, context):
        super().configure(context)
        self.TRIG = self.trig()
        self.ECHO = self.echo()
        self.logger.debug(self.TRIG)
        self.logger.debug(self.ECHO)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def stop(self):
        super().stop()
        GPIO.cleanup()

    def process_signals(self, signals):
        for signal in signals:
            GPIO.output(self.TRIG, False)
            #TRIGGER
            GPIO.output(self.TRIG, True)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, False)
            # todo: first measurement does not work, pulse_start = None
            while GPIO.input(self.ECHO) == 0:
               self.pulse_start = time.time()

            while GPIO.input(self.ECHO) == 1:
               self.pulse_end = time.time()

            pulse_length = self.pulse_end - self.pulse_start
            #17150 = 1/2 speed of sound due to two trips of the sound
            distance = pulse_length * 17150
            distance = round(distance, 2) #for cm

            self.notify_signals([ Signal( { "distance" : distance } )])
