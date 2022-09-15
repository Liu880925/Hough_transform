import cv2
import numpy as np
img  = cv2.imread('test.jpg')
img1 = img.copy()
img2 = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
blurred  = cv2.GaussianBlur(gray, (5, 5), 0)
canny = cv2.Canny(blurred, 80, 100)

mask = np.zeros([canny.shape[0], canny.shape[1]], dtype=np.uint8)
x_data = np.array([190, 270, 325, 570])
y_data = np.array([450, 315, 315, 450])
pts = np.vstack((x_data, y_data)).astype(np.int32).T
cv2.fillPoly(mask, [pts], (255), 8, 0)
roi_mask = cv2.bitwise_and(canny, canny, mask=mask)

lines = cv2.HoughLines(roi_mask, 4, np.pi/180, 90)
for line in lines:
    rho = line[0][0]
    theta = line[0][1]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img1, (x1, y1), (x2, y2), (0, 0, 255), 2)

lines = cv2.HoughLinesP(roi_mask,rho=5,threshold=85,theta=np.pi/180,minLineLength=3,maxLineGap=2,lines=np.array([]))
for line in lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[0][2]
    y2 = line[0][3]
    cv2.line(img2, (x1, y1), (x2, y2), (0, 255, 255), 2)
    
cv2.imshow('houghlines3', img1)
cv2.imshow('edges', img2)
cv2.waitKey(0)
#cv2.imwrite('HoughLinesP_better.jpg', img2)