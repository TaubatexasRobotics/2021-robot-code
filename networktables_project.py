#!/usr/bin/env python3
#
# This is a NetworkTables server (eg, the robot or simulator side).
#
# On a real robot, you probably would create an instance of the
# wpilib.SmartDashboard object and use that instead -- but it's really
# just a passthru to the underlying NetworkTable object.
#
# When running, this will continue incrementing the value 'robotTime',
# and the value should be visible to networktables clients such as
# SmartDashboard. To view using the SmartDashboard, you can launch it
# like so:
#
#     SmartDashboard.jar ip 127.0.0.1
#

import time
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
#NetworkTables.initialize(server='10.74.59.2')
sd = NetworkTables.getTable("SmartDashboard")

#sd.putNumber("robotValue",1) 
'''
while True:
    print("dsTime:", sd.getNumber("robotTime", -1))

    sd.putNumber("robotTime", i)
    time.sleep(1)
    i += 1
'''
