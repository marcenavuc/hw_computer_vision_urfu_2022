import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

import cv2


@dataclass
class Rect:
    start_point: list[int, int]
    end_point: list[int, int]
    finger_id: int


class AbstractFingerStrategy(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplemented

    @property
    def score(self):
        raise NotImplemented

    @property
    def is_end(self):
        raise NotImplemented

    @abstractmethod
    def update(self, fingers):
        raise NotImplemented


# TODO: add color in rect
class RectStrategy(AbstractFingerStrategy):
    RECT_COLORS = {
        8: (127, 66, 135),
        12: (0, 207, 255),
        16: (0, 255, 0),
        20: (195, 97, 24),
    }

    def __init__(self,
                 n_rects: int,
                 width: int,
                 height: int,
                 start_speed: float,
                 acceleration: float):
        self.max_rects = n_rects
        self.start_speed = start_speed
        self.acceleration = acceleration
        self.width = width
        self.height = height

        self.speed = start_speed
        self.rect_width = 40
        self.border = 20
        self._score = 0
        self._is_end = False
        self.rects = []

    @property
    def score(self):
        return self._score

    @property
    def is_end(self):
        return self._is_end

    def update(self, fingers):
        for _ in range(self.max_rects - len(self.rects)):
            self.make_rect()
        self.move_rects()
        self.collide_finger_with_rect(fingers)
        self.check_is_end()

    def check_is_end(self):
        for rect in self.rects:
            if rect.end_point[1] >= self.height:
                self._is_end = True

    def draw(self, image):
        for rect in self.rects:
            cv2.rectangle(
                image,
                rect.start_point,
                rect.end_point,
                self.RECT_COLORS[rect.finger_id]
            )

    def make_rect(self):
        random_x = random.randint(self.border, self.width - self.border)
        random_height = random.randint(self.border, self.height)
        color_id = list(self.RECT_COLORS.keys())
        new_rect = Rect(
            start_point=[random_x, -random_height],
            end_point=[random_x + self.rect_width, 0],
            finger_id=random.choice(color_id)
        )
        self.rects.append(new_rect)

    def move_rects(self):
        for rect in self.rects:
            rect.start_point[1] += int(self.speed)
            rect.end_point[1] += int(self.speed)
        self.speed += self.acceleration

    def collide_finger_with_rect(self, fingers: dict[list[int, int]]):
        delete_rects = []
        for rect in self.rects:
            if rect.finger_id not in fingers:
                continue
            finger = fingers[rect.finger_id]
            if rect.start_point[0] < finger[0] < rect.end_point[0] \
                    and rect.start_point[1] < finger[1] < rect.end_point[1]:
                self._score += abs(finger[1] - rect.end_point[1])
                rect.end_point[1] = finger[1]

                if abs(rect.start_point[1] - rect.end_point[1]):
                    delete_rects.append(rect)
        for rect in delete_rects:
            self.rects.remove(rect)
