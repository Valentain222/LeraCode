import cv2
import numpy as np

lower_red = np.array([20, 25, 180])
upper_red = np.array([179, 180, 255])

frame = cv2.imread("87137956.jpg")
cv2.imshow("123124", frame)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT_ALT, 1, 20, param1=500, param2=0.5, minRadius=1, maxRadius=500)
circles = np.uint16(np.around(circles))

mask = cv2.inRange(frame, lower_red, upper_red)
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
cv2.imshow("mask", mask)

for i in circles[0,:]:
    # draw the outer circle
    # cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    # cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
    part = frame[(i[1]-i[2]):(i[1]+i[2]), (i[0]-i[2]):(i[0]+i[2])]
    part = cv2.resize(part, (20, 20))
    red = cv2.extractChannel(part, 2)
    print(np.sum(red))
    cv2.imshow("part", part)
    cv2.imshow("red", red)
    cv2.waitKey(0)
 
cv2.imshow('detected circles',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()