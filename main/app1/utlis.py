import cv2
import mediapipe as mp
import numpy as np
import math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

current_status = "Unknown"


cap = cv2.VideoCapture(0)  


def calculate_forward_angle(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    angle = abs(math.degrees(math.atan2(dx, dy)))
    return angle

def get_frame_and_status():
    global current_status

    if not cap.isOpened():
        return None, "Camera not opened"

    ret, frame = cap.read()
    if not ret:
        return None, "Failed to capture frame"

    frame = cv2.resize(frame, (640, 480))
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        h, w, _ = frame.shape
        lm = results.pose_landmarks.landmark

        shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        ear = lm[mp_pose.PoseLandmark.RIGHT_EAR]

        if shoulder.visibility > 0.5 and ear.visibility > 0.5:
            shoulder_px = (int(shoulder.x * w), int(shoulder.y * h))
            ear_px = (int(ear.x * w), int(ear.y * h))

            neck_forward_angle = calculate_forward_angle(ear_px, shoulder_px)

            if neck_forward_angle < 25:
                current_status = "✅ Good posture"
            else:
                current_status = "⚠️ Slouch detected!"

            # Draw points & line
            cv2.circle(image, ear_px, 6, (0, 0, 255), -1)
            cv2.circle(image, shoulder_px, 6, (0, 255, 0), -1)
            cv2.line(image, ear_px, shoulder_px, (255, 255, 0), 2)
            cv2.putText(image, f"{current_status} ({int(neck_forward_angle)}°)",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            current_status = "⚠️ Not visible"

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    else:
        current_status = "⚠️ No landmarks"

    return image, current_status