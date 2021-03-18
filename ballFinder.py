import argparse
import cv2
#import imutils

def ballPosition(frame, draw=False ):
    frameSizeX = len(frame[1])

    yellowLower = (20, 100, 100)
    yellowUpper = (30, 255, 255)

    # resize the frame, blur it, and convert it to the HSV color space
    #frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    # perform a series of dilations and erosions to remove any small blobs left in the mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:

        c = max(cnts, key=cv2.contourArea)

        ((x, y), circleRadius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if circleRadius > 20:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            if(draw):
                cv2.circle(frame, (int(x), int(y)), int(circleRadius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
                cv2.imshow("Frame", frame)
                cv2.imshow("Mask", mask)
            
            if(center):
                centerX = center[0]
                relativeX = centerX / frameSizeX
                relativeRadius = circleRadius/frameSizeX   
                return relativeX, relativeRadius
            return None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())
    
    # if a video path was not supplied, use the webcam
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)
    # otherwise, grab a reference to the video file
    else:
        camera = cv2.VideoCapture(args["video"])
    
# infinite loop
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        
        if args.get("video") and not grabbed:
            break
    
        print(ballPosition(frame, draw=True))
            
        window_name="Frame"
        # show the frame to our screen
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        #cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)
        

        key = cv2.waitKey(1) & 0xFF
    
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
    
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()