from dataclasses import dataclass

import cv2
import av
import mediapipe as mp

from .rect import RectStrategy

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
)

BLOCK_COLORS = [
    (125, 70, 117),
    (254, 203, 3),
    (0, 255, 0),
    (0, 0, 255),
]

@dataclass
class Rect:
    start_point: list
    end_point: list
    finger_id: int


class VideoProcessor:
    FINGERS_ID = [8, 12, 16, 20]
    WIDTH = 480
    HEIGHT = 640

    def __init__(self):
        self.game = RectStrategy(
            n_rects=3,
            width=self.WIDTH,
            height=self.HEIGHT,
            start_speed=1,
            acceleration=0.0001,
        )

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = self.process(img)
        return av.VideoFrame.from_ndarray(img, format="rgb24")

    def draw_fingers(self, image, hands):
        if len(hands) == 0:
            return image

        mp_drawing.draw_landmarks(
            image,
            hands[0],
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )
        return image

    def get_hand(self, image):
        process_result = hands.process(image)
        if process_result.multi_hand_landmarks:
            return process_result.multi_hand_landmarks
        return []

    def get_fingers(self, hands: list):
        if len(hands) == 0:
            return []
        landmarks = list(hands[0].landmark)

        return {i: [
                    int(landmarks[i].x * self.HEIGHT),
                    int(landmarks[i].y * self.WIDTH)]
                for i in self.FINGERS_ID}

    def draw_final_scene(self, image):
        cv2.putText(
            image,
            "WASTED",
            (self.WIDTH//2 - 20, self.HEIGHT//2 - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
            cv2.LINE_AA
        )
        cv2.putText(
            image,
            "PRESS F5 TO RESTART",
            (self.WIDTH//2 - 20, self.HEIGHT//2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
            cv2.LINE_AA
        )

    def draw_score(self, image):
        cv2.putText(
            image,
            f"SCORE: {self.game.score}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    def process(self, image):
        if not self.game.is_end:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)

            hands = self.get_hand(image)
            image = self.draw_fingers(image, hands)

            fingers = self.get_fingers(hands)
            self.game.update(fingers)
            self.game.draw(image)
            self.draw_score(image)
        else:
            self.draw_final_scene(image)

        return image
