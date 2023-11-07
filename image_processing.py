import cv2
import mediapipe as mp
import numpy as np

from PIL import Image


class AmputationAngleCalculator:
    def __init__(self, uploaded_file):
        self.image = self.LoadingImage(uploaded_file)
        self.mp_pose, self.pose_landmarks = self.PoseLandmarks(self.image)
        self.visibility_threshold = .5

    def LoadingImage(self, uploaded_file):
        try:
            image = Image.open(uploaded_file)
            image = np.array(image)
            if image.shape[-1] != 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return image
        except Exception as e:
            print(f"Error loading: {e}")
            return None

    def PoseLandmarks(self, image):
        mp_pose = mp.solutions.pose
        with mp_pose.Pose(static_image_mode=True,
                          model_complexity=2,
                          enable_segmentation=True) as pose:
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        return mp_pose, results.pose_landmarks

    def draw_landmarks(self):
        annotated_image = self.image.copy()
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_drawing.draw_landmarks(annotated_image,
                                  self.pose_landmarks,
                                  self.mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                                  )
        return annotated_image

    def LandmarkCoordinates(self, landmark_name):
        try:
            lm = self.pose_landmarks.landmark[landmark_name]
            if lm.visibility < self.visibility_threshold:
                return None
            else:
                return lm
        except KeyError:
            return None

    def calculate_angle(self):
        left_ankle = self.LandmarkCoordinates(self.mp_pose.PoseLandmark.LEFT_ANKLE)
        right_ankle = self.LandmarkCoordinates(self.mp_pose.PoseLandmark.RIGHT_ANKLE)

        if left_ankle is not None and right_ankle is not None:
            return 'no_limb', left_ankle, right_ankle
        elif left_ankle is None and right_ankle is None:
            return 'no_ankles', left_ankle, right_ankle
        else:
            if left_ankle is None:
                hip = self.LandmarkCoordinates(self.mp_pose.PoseLandmark.LEFT_HIP)
                knee = self.LandmarkCoordinates(self.mp_pose.PoseLandmark.LEFT_KNEE)
            elif right_ankle is None:
                hip = self.LandmarkCoordinates(self.mp_pose.PoseLandmark.RIGHT_HIP)
                knee = self.LandmarkCoordinates(self.mp_pose.PoseLandmark.RIGHT_KNEE)

        if hip is None or knee is None:
            return None

        femur_vector = (knee.x - hip.x, knee.y - hip.y)
        angle_rad = np.arctan2(femur_vector[1], femur_vector[0]) - np.pi/2
        angle_degrees = np.degrees(angle_rad)

        return angle_degrees
