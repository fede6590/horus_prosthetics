import cv2
import numpy as np


class AngleCalculator:
    def __init__(self, image_path):
        self.image = cv2.imdecode(
            np.fromstring(image_path.read(), np.uint8),
            cv2.IMREAD_COLOR
            )

    def visualize_keypoints(self):
        # Detect keypoints and descriptors
        detector = cv2.ORB_create()
        image_keypoints, descriptors = detector.detectAndCompute(self.image, None)

        # Draw lines to visualize the keypoints
        image_with_keypoints = cv2.drawKeypoints(self.image, image_keypoints, self.image)

        return image_with_keypoints

    def calculate_angle(self):
        # Convert the image to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Apply a Canny edge detector to the image
        edges = cv2.Canny(gray, 50, 150)

        # Find the contours in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter the contours to find the two largest contours in the image
        filtered_contours = []
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                filtered_contours.append(contour)

        if len(filtered_contours) >= 2:
            # Draw lines over the two largest contours in the image
            for contour in filtered_contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.line(self.image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Calculate the angle between the two lines
            angle = cv2.phase(filtered_contours[0][:, 0], filtered_contours[1][:, 0]) * 180 / np.pi

            return self.image, angle
        else:
            return self.image, None
