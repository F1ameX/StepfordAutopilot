import numpy as np
import cv2
from PIL import ImageGrab


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

    cv2.imshow('window_new', cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))
    cv2.imshow('Traffic Light', traffic_light_image)
    cv2.imshow('Speedometer', speedometer_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
