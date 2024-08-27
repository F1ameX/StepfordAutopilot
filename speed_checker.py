import cv2
import numpy as np
import time
import pyautogui as gw
from util import *

gw.PAUSE = 0.01


def find_speed_limit(roi_image):
    green_color = np.array([0, 255, 0])
    red_color = np.array([0, 0, 255])

    hsv_image = cv2.cvtColor(roi_image, cv2.COLOR_RGB2HSV)

    red_lower_limit, red_upper_limit = get_color_limits(red_color)
    red_mask = cv2.inRange(hsv_image, red_lower_limit, red_upper_limit)

    green_lower_limit, green_upper_limit = get_color_limits(green_color)
    green_mask = cv2.inRange(hsv_image, green_lower_limit, green_upper_limit)

    full_mask = red_mask | green_mask

    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(full_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_contour = min(red_contours, key=cv2.contourArea)
    green_contour = min(green_contours, key=cv2.contourArea)
    max_contour = min(contours, key=cv2.contourArea)

    red_x, red_y, red_w, red_h = cv2.boundingRect(red_contour)
    green_x, green_y, green_w, green_h = cv2.boundingRect(green_contour)
    x, y, w, h = cv2.boundingRect(max_contour)

    cv2.rectangle(full_mask, (x, y), (x + w, y + h), (255, 0, 0), 1)
    print(green_x, red_x)
    if len(contours) == 1:
        return 1
    elif green_y < red_y:
        return 2
    elif green_y > red_y:
        return 3

    cv2.imshow("Red speed limit point", full_mask)


def set_speed(roi_image):
    speed_condition = find_speed_limit(roi_image)
    print(speed_condition, end=' condition\n')
    if speed_condition == 2:
        for i in range(1, 8):
            gw.press('s')
    elif speed_condition == 3:
        for i in range(1, 24):
            gw.press('w')






