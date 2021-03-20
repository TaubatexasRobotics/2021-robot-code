#!/usr/bin/env python3
#
# Uses the CameraServer class to automatically capture video from a USB webcam
# and send it to the FRC dashboard without doing any vision processing.
#
# Warning: If you're using this with a python-based robot, do not run this
# in the same program as your robot code!
#

'''
/dev/v4l
/dev/v4l/by-id
/dev/v4l/by-id/usb-Generic_Web_Camera_200901010001-video-index1
/dev/v4l/by-id/usb-Generic_Web_Camera_200901010001-video-index0
/dev/v4l/by-path
/dev/v4l/by-path/pci-0000:00:14.0-usb-0:5:1.0-video-index1
/dev/v4l/by-path/pci-0000:00:14.0-usb-0:5:1.0-video-index0

find /dev/v4l
'''




from cscore import CameraServer


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    cs.startAutomaticCapture(name='cam1', path='/dev/v4l/by-id/usb-Generic_Web_Camera_200901010001-video-index0')
    cs.waitForever()


if __name__ == "__main__":

    # To see messages from networktables, you must setup logging
    import logging

    loAgging.basicConfig(level=logging.DEBUG)

    # You should uncomment these to connect to the RoboRIO
    #import networktables
    #networktables.initialize(server='127.0.0.1')

    main()
