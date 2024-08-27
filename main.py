import numpy as np
import pyautogui as gw
import cv2
from PIL import ImageGrab
from util import *
from speed_checker import *


def detect_traffic_light_color(roi_image):
    red_color = np.array([255, 0, 0])
    yellow_color = np.array([255, 255, 0])
    green_color = np.array([0, 255, 0])

    hsv_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2HSV)

    red_lower_limit, red_upper_limit = get_color_limits(red_color)
    yellow_lower_limit, yellow_upper_limit = get_color_limits(yellow_color)
    green_lower_limit, green_upper_limit = get_color_limits(green_color)

    red_mask = cv2.inRange(hsv_image, red_lower_limit, red_upper_limit)
    yellow_mask = cv2.inRange(hsv_image, yellow_lower_limit, yellow_upper_limit)
    green_mask = cv2.inRange(hsv_image, green_lower_limit, green_upper_limit)

    red_pixels = cv2.countNonZero(red_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    green_pixels = cv2.countNonZero(green_mask)

    if red_pixels > max(yellow_pixels, green_pixels):
        return 1
    elif yellow_pixels > max(red_pixels, green_pixels):
        return 2
    elif green_pixels > max(red_pixels, yellow_pixels):
        return 3


def aws_system_skipper(roi_image):
    yellow_color = np.array([255, 255, 0])
    hsv_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2HSV)
    yellow_lower_limit, yellow_upper_limit = get_color_limits(yellow_color)
    yellow_mask = cv2.inRange(hsv_image, yellow_lower_limit, yellow_upper_limit)
    yellow_pixels = cv2.countNonZero(yellow_mask)

    if yellow_pixels > 15:
        gw.press('q')
    cv2.imshow("Yellow mask AWS", yellow_mask)


def process_roi(image, roi):
    x, y, w, h = roi
    roi_image = image[y:y+h, x:x+w]
    rgb_roi = cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB)
    return rgb_roi


while True:
    window = ImageGrab.grab(bbox=(920, 60, 1920, 725))
    img_np = np.array(window)

    traffic_light = (220, 520, 60, 130)
    speedometer = (750, 425, 760, 430)

    traffic_light_image = process_roi(img_np, traffic_light)
    speedometer_image = process_roi(img_np, speedometer)

    aws_system_skipper(speedometer_image)
    set_speed(speedometer_image)

    traffic_light_color = detect_traffic_light_color(traffic_light_image)
    print(traffic_light_color)
    cv2.imshow('Traffic Light', traffic_light_image)

    if cv2.waitKey(1) & 0xFF == ord('`'):
        cv2.destroyAllWindows()
        break
