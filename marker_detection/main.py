import cv2
import numpy as np


GREEN_COLOR = (0, 255, 0)


def process_image(image: np.array) -> np.array:
    green_marker_mask: np.array = (
        (image[:, :, 0] < 90)
      & (image[:, :, 1] > 95)
      & (image[:, :, 2] < 100)
    )
    red_marker_mask: np.array = (
        (image[:, :, 0] > 5)
      & (image[:, :, 1] < 250)
      & (image[:, :, 2] < 255)
    )
    result = np.zeros(shape=image.shape)
    result[green_marker_mask | ~red_marker_mask] = 255
    return result


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
