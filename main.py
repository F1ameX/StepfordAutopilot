import numpy as np
import pyautogui as gw
import cv2
import time
from PIL import ImageGrab


def get_color_limits(color):
    color = np.uint8([[color]])
    hsv_color = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)
    hue = hsv_color[0][0][0]

    if hue >= 165:
        lower_limit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_limit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:
        lower_limit = np.array([0, 100, 100], dtype=np.uint8)
        upper_limit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lower_limit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_limit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lower_limit, upper_limit


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

    if yellow_pixels > 0:
        gw.press('q')


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
    traffic_light_color = detect_traffic_light_color(traffic_light_image)

    cv2.imshow('Traffic Light', traffic_light_image)
    cv2.imshow('Speedometer', speedometer_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
