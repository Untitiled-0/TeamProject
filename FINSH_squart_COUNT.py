import cv2                  #영상 관련 라이브러리
import mediapipe as mp      # MEDIAPIPE 라는 솔루션 : 누군가가 만든거야
import numpy as np # 숫자, 계산 관련 라이브러리
import winsound
import time

mp_drawing = mp.solutions.drawing_utils     #
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(1)

squart_count = 0
state = None


def left_calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    left_leg_angle = np.abs(radians * 180.0 / np.pi)

    if left_leg_angle > 180.0:
        left_leg_angle = 360 - left_leg_angle

    return left_leg_angle

## Setup mediapipe instance

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():

        ret, frame = cap.read()
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            left_foot_index_x = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x]
            left_foot_index_y = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            left_knee_x = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x]
            left_knee_y = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            # LEFT, RIGHT Calculate angle
            left_waist_angle = left_calculate_angle(left_shoulder, left_hip, left_knee)
            left_angle = left_calculate_angle(left_hip, left_knee, left_ankle)

            cv2.putText(image, str(int(left_angle)),
                        tuple(np.multiply(left_knee, [960, 240]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            if left_angle > 160:
                state = 'stand'
            if 90 < left_angle < 110 and state == 'stand':
                state = 'squart'
                squart_count += 1
                m = left_knee_x[0] - left_foot_index_x[0]
                if m < -0.02:
                    winsound.PlaySound("djdejddl.wav",winsound.SND_ASYNC)
                elif (left_waist_angle < 100):
                    winsound.PlaySound("gjfl.wav",winsound.SND_ASYNC)
                else:
                    pass
        except:
            pass
        cv2.rectangle(image, (0, 0), (225, 73), (255, 255, 255), -1)

        # Rep data
        cv2.putText(image, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(squart_count),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(image, 'STATE', (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, state,
                    (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('SMART PT', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()