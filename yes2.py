import pyrealsense2 as rs
import numpy as np
import cv2
from vars import *

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

def detect(lowerHSV, upperHSV):
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    #if not depth_frame or not color_frame:
        #continue
    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    #convert color image to hsv 
    hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerHSV, upperHSV)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    _, conts, _= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    res = cv2.bitwise_and(color_image, color_image, mask=mask)

    gray = cv2.medianBlur(hsv, 5)
    rows = gray.shape()
    
    return mask, res, conts, color_image, depth_image, gray, rows

def drawContours(conts, color_image):
    for i in range(len(conts)):
        c = max(conts,key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #only run of it is a certain size
        if radius > 200:
            x,y,w,h=cv2.boundingRect(conts[i])
            cv2.rectangle(color_image,(x,y),(x+w,y+h),(0,0,255), 2)
            xcenter = (int(M["m10"] / M["m00"]))
            print(xcenter)
            xOffset = int(xcenter - middleOfRes)
            print(xOffset)                    
            return xcenter        
        else:
            pass
            #break

def detectCircles(gray, rows, color_image):
    circles = cv2.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30, minRadius=1, maxRadius=30)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(color_image, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(color_image, center, radius, (255, 0, 255), 3)


while True:
    #detect green
    mask, res, conts, color_image, depth_image, gray, rows = detect(l_red, u_red)

    xcenter = drawContours(conts, color_image)

    detectCircles(gray, rows, color_image)

    cv2.imshow("detected circles", color_image)
    cv2.imshow('frame', color_image)
    cv2.imshow('mask', mask)   
    cv2.imshow('res', res)
    cv2.waitKey(1)
