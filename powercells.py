# import the necessary packages
from collections import deque
import numpy as np
import cv2

# lower and upper boundaries of the "yellow" in HSV
yellowLower = (20, 100, 100)
yellowUpper = (30, 255, 255)

# use the webcam
camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
# infinite loop
while True:
    # grab the current frame   -- propriedades
    (grabbed, frame) = camera.read()
    
    # resize the frame, blur 
    #  it, and convert it to the HSV color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = None
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        NBolas = 3
        c = []
        listaDeContornos = [((0, 0), 0),
                            ((0, 0), 0),
                            ((0, 0), 0)]
        center = []
        maximo = 0
        for countour in range(NBolas):
            bolas_suficientes = True
            try:
                maximo = max(cnts, key=cv2.contourArea)

            except:
                bolas_suficientes = False
                if countour>0:
                    print("Há apenas {} bolas".format(countour))
                else:
                    print("Não há bolas")
            
            if(bolas_suficientes):
                c.append(maximo)
                listaDeContornos[countour]=(cv2.minEnclosingCircle(maximo))
                m = cv2.moments(maximo)
                center.append((int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])))
                try:
                    cnts.remove(maximo)
                    if countour==2:
                        print("Deu tudo certo")
                except:
                    print("ops, este é o", countour )
        # only proceed if the radius meets a minimum size
        i=0
        for contorno in listaDeContornos:
            radius = contorno[1]
            x = contorno[0][0]
            y = contorno[0][1]
            if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center[i], 5, (0, 0, 255), -1)
            i+=1
   
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    # cv2.imshow("Frame", mask)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

