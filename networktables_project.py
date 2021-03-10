import time
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize(server='localhost')
sd = NetworkTables.getTable("SmartDashboard")

i = 0
while True:
    print("dsTime:", sd.getNumber("robotTime", -1))

    sd.putNumber("robotTime", i)
    time.sleep(1)
    i += 1

