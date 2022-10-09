import cv2
import numpy as np


GREEN_COLOR = (0, 255, 0)


def draw_rect(image: np.array, mask: np.array) -> np.array:
    try:
        idxs_x = np.argmax(mask, axis=0)
        idxs_y = np.argmax(mask, axis=1)

        idxs_x = idxs_x[idxs_x > 0]
        idxs_y = idxs_y[idxs_y > 0]

        result = cv2.rectangle(image,
                               (idxs_y.min(), idxs_x.min()),
                               (idxs_x.max(), idxs_x.max()),
                               GREEN_COLOR, 3)
    except ValueError:
        print("Got error")


def process_image(image: np.array) -> np.array:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv,
                           np.array([0, 90, 140]),
                           np.array([20, 255, 255])
    )
    green_mask = cv2.inRange(hsv,
                             np.array([40, 70, 20]),
                             np.array([80, 255, 255])
    )
    draw_rect(image, red_mask)
    draw_rect(image, green_mask)

    return green_mask | red_mask


def main():
    imcap = cv2.VideoCapture(0)
    imcap.set(3, 320)
    imcap.set(4, 240)

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
