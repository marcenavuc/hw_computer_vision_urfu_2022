import cv2
import numpy as np


GREEN_COLOR = (0, 255, 0)


def process_image(image: np.array) -> np.array:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv,
                           np.array([0, 90, 140]),
                           np.array([20, 255, 255])
    )
    green_mask = cv2.inRange(hsv,
                             np.array([40, 60, 20]),
                             np.array([90, 255, 255])
    )

    return green_mask | red_mask


def main():
    imcap = cv2.VideoCapture(0)
    imcap.set(3, 640)
    imcap.set(4, 480)

    while True:
        success, img = imcap.read()

        processed_image = process_image(img)
        cv2.imshow('marker_detection1', img)
        cv2.imshow('marker_detection', processed_image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    imcap.release()
    cv2.destroyWindow('marker_detection')


if __name__ == '__main__':
    main()
