import cv2
import pytesseract


def recognize_distance_to_traffic_light(roi_image):
    numbers_cfg = r'--oem 3 --psm 6 outputbase digits'
    gray_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(thresh, config=numbers_cfg)
    if len(text) > 1:
        distance = text.split('\n')[1]
        return distance


def recognize_distance_to_next_station(roi_image):
    numbers_cfg = r'--oem 3 --psm 6 outputbase digits'
    gray_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(thresh, config=numbers_cfg)
    print(text)
