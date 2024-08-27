import cv2
import numpy as np
from util import *


def find_speed_limit(roi_image):
    green_color = np.array([0, 255, 0])
    red_color = np.array([0, 0, 255])

    hsv_image = cv2.cvtColor(roi_image, cv2.COLOR_RGB2HSV)

    red_lower_limit, red_upper_limit = get_color_limits(red_color)
    red_mask = cv2.inRange(hsv_image, red_lower_limit, red_upper_limit)

    green_lower_limit, green_upper_limit = get_color_limits(green_color)
    green_mask = cv2.inRange(hsv_image, green_lower_limit, green_upper_limit)

    full_mask = red_mask | green_mask

    contours, _ = cv2.findContours(full_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = min(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    print(x, y, w, h, end='\n')
    cv2.rectangle(full_mask, (x, y), (x + w, y + h), (255, 0, 0), 1)

    if len(contours) == 1:
        print("Setted normal speed")

    cv2.imshow("Red speed limit point", full_mask)
    return x, y, w, h







