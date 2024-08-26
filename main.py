import numpy as np
import cv2
from PIL import ImageGrab


def detect_traffic_light_color(roi_image):
    hsv_image = cv2.cvtColor(roi_image, cv2.COLOR_RGB2HSV)

    red_lower_1 = np.array([0, 100, 100])
    red_upper_1 = np.array([10, 255, 255])
    red_lower_2 = np.array([160, 100, 100])
    red_upper_2 = np.array([179, 255, 255])

    yellow_lower = np.array([10, 50, 50])
    yellow_upper = np.array([40, 255, 255])

    green_lower = np.array([40, 100, 100])
    green_upper = np.array([70, 255, 255])

    red_mask_1 = cv2.inRange(hsv_image, red_lower_1, red_upper_1)
    red_mask_2 = cv2.inRange(hsv_image, red_lower_2, red_upper_2)
    red_mask = cv2.bitwise_or(red_mask_1, red_mask_2)

    yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv_image, green_lower, green_upper)

    red_pixels = cv2.countNonZero(red_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    green_pixels = cv2.countNonZero(green_mask)

    if red_pixels > max(yellow_pixels, green_pixels):
        print("Red Color RN")
    elif yellow_pixels > max(red_pixels, green_pixels):
        print("Yellow Color RN")
    elif green_pixels > max(red_pixels, yellow_pixels):
        print("Green color RN")


def process_roi(image, roi):
    x, y, w, h = roi
    roi_image = image[y:y+h, x:x+w]
    gray_roi = cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB)
    return gray_roi


while True:
    window = ImageGrab.grab(bbox=(920, 60, 1920, 725))
    img_np = np.array(window)

    traffic_light = (220, 520, 60, 130)
    speedometer = (750, 425, 760, 430)

    traffic_light_image = process_roi(img_np, traffic_light)
    speedometer_image = process_roi(img_np, speedometer)

    detect_traffic_light_color(traffic_light_image)

    cv2.imshow('Traffic Light', traffic_light_image)
    cv2.imshow('Speedometer', speedometer_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
