import cv2
import numpy as np


def draw(mask, color, frame):
    contours, _ = cv2.cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
         area = cv2.contourArea(c)
         if area > 1000:
             new_contour = cv2.convexHull(c)
             cv2.drawContours(frame, [new_contour], 0, color, 3)



def capture():
    cap = cv2.VideoCapture(0)
    low_yellow = np.array([25,192,20], np.uint8)
    high_yellow = np.array([30,255,255], np.uint8)
    low_red1 = np.array([0,100,20], np.uint8)
    high_red1 = np.array([5,255,255], np.uint8)
    low_red2 = np.array([175,100,20], np.uint8)
    high_red2 = np.array([180,255,255], np.uint8)


    while True:
        comp, frame = cap.read()
        if comp == True:
            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            yellow_mask= cv2.inRange(frame_HSV, low_yellow, high_yellow)
            red_mask1= cv2.inRange(frame_HSV, low_red1, high_red1)
            red_mask2= cv2.inRange(frame_HSV, low_red2, high_red2)
            red_mask = cv2.add(red_mask1, red_mask2)




            draw(yellow_mask, [0,255,255], frame)
            draw(red_mask,[0, 0, 255], frame)

            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
                cap.release()
                cv2.destroyAllWindows()
