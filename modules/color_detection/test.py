import numpy as np
import cv2
from color_rectangle_finder import *

cap = cv2.VideoCapture(3)

##blue color##
#np.array([220,20,20]
#np.array([260,100,100])
####

##red color##
#np.array([0,68,56]
#np.array([11,100,100])
####

while(True):
    _, frame = cap.read()

    #blue color
    # low_range = np.array([220,20,20])
    # high_range = np.array([260,100,100])
    #red color
    low_range = np.array([0,20,20])
    high_range = np.array([11,100,100])
    low = fit_2_hsv(low_range)
    high = fit_2_hsv(high_range)

    rects = find_rectangles_by_color(frame, low_range, high_range,20,20)        
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, low, high)

    # Bitwise-AND mask and original image
    output = cv2.bitwise_and(frame,frame, mask= mask)

    # Blue color in BGR
    color = (255, 255, 255)
    
    # Line thickness of 2 px
    thickness = 3
    for rect in rects:
        output = cv2.rectangle(output, (rect[1], rect[0]), (rect[3], rect[2]), color, thickness)
    
    # Display the frame
    cv2.imshow('output',output)

    if cv2.waitKey(1) & 0xFF == ord('Q'):
      break

# Closes all the frames
cv2.destroyAllWindows() 



