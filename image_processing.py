import cv2
import mediapipe as mp
import numpy as np

from PIL import Image


class AmputationAngleCalculator:
    def __init__(self, uploaded_file):
        self.image = self.LoadingImage(uploaded_file)
        self.image = self.VerticalAxis()

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

    def VerticalAxis(self):
        # Convert the image to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # Apply Canny edge detection
        edges = cv2.Canny(gray, threshold1=30, threshold2=100)
        # Apply Hough Line Transform to find vertical lines
        lines = cv2.HoughLinesP(edges, 1, np.pi/2, threshold=50, minLineLength=100, maxLineGap=10)

        if lines is not None:
            # Find the longest vertical line
            max_length = 0
            best_line = None
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = abs(x2 - x1)
                if length > max_length:
                    max_length = length
                    best_line = line

            if best_line is not None:
                x1, y1, x2, y2 = best_line[0]
                cv2.line(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red line for the best line

        return self.image

    def draw_landmarks(self):
        if self.image is None:
            return None

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose

        with mp_pose.Pose(static_image_mode=True,
                          model_complexity=2,
                          enable_segmentation=True) as pose:

            # Convert the image to RGB and then process with the `Pose` object.
            results = pose.process(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))

        # Copy the image
        annotated_image = self.image.copy()

        # Draw pose, left and right hands, and face landmarks on the image with drawing specification defaults.
        mp_drawing.draw_landmarks(annotated_image,
                                  results.pose_landmarks,
                                  mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                                  )
        return annotated_image

    def calculate_angle(self):
        return 'pepe'
