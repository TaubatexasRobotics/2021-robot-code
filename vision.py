# Import the camera server, OpenCV, NumPy and argparse
import cscore
import cv2
import numpy as np
import argparse
import networktables_project

def ballPosition(frame):
    frameSizeX = len(frame[1])
    frameSixeY = frame.shape[0]
    yellowLower = (20, 100, 100)
    yellowUpper = (30, 255, 255)
    
    # resize the frame, blur it, and convert it to the HSV color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    # perform a series of dilations and erosions to remove any small blobs left in the mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    cnts = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), circleRadius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if circleRadius > 10:
            # then update the list of tracked points
            if(center):
                relativeX = center [0]/ frameSizeX
                relativeY = center[1] / frameSixeY
                relativeRadius = circleRadius/frameSizeX   
                return relativeX, relativeRadius, relativeY
    return (-1, -1, -1)

def main():

    RESOLUCOES_POSSIVEIS = {'baixa':(160, 120), 'media':(320,240), 'alta':(640,480)}
    RESOLUCAO = RESOLUCOES_POSSIVEIS['alta']

    cs = cscore.CameraServer.getInstance()
    cs.enableLogging()

    # Capture from the first USB Camera on the system
    camera = cs.startAutomaticCapture()
    
    # Set the video mode and resolution of camera
    config = cscore.VideoMode(cscore.VideoMode.PixelFormat.kYUYV, *RESOLUCAO, 15)
    camera.setVideoMode(config)

    #camera.setResolution(320, 240)

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("vision.py-camera", *RESOLUCAO)

    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(*RESOLUCAO, 3), dtype=np.uint8)
    
    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError());
            # skip the rest of the current iteration
            continue
        
        relativeX, relativeRadius, relativeY = ballPosition(img)
        networktables_project.sd.putNumber("robotX",relativeX)
        networktables_project.sd.putNumber("radius",relativeRadius) 
        networktables_project.sd.putNumber("robotY",relativeY)
