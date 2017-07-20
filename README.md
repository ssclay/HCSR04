HCSRO4
===========

Ultrasonically measure distance using the HC-SRO4 Range finder and the GPIOs of a Raspberry PI

Properties
--------------
trig : Trigger GPIO, GPIO pin number used to trigger the Measurement
echo : Echo GPIO, Input pin number to the Raspberry Pi

Dependencies
----------------
RPi.GPIO

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
distance : float, distance in cm.
