from flask import Flask, render_template, Response
import cv2
import numpy as np
import mediapipe as mp
import sys
app = Flask(__name__)

# Load a sample picture and learn how to recognize it.

process_this_frame = True

def gen_frames():
    # pi = pigpio.pi()

    mp_drawing = mp.solutions.drawing_utils  #
    mp_pose = mp.solutions.pose

    # pygame.mixer.init()
    #
    # motorL = Motor(forward=20, backward=21)
    # motorR = Motor(forward=19, backward=26)
    #
    # p_s = pygame.mixer.Sound('wjdaus.wav')
    # p_s1 = pygame.mixer.Sound('djdejddl.wav')
    # p_s2 = pygame.mixer.Sound('gjfl.wav')
    # p_s4 = pygame.mixer.Sound('dhfmsWhr.wav')
    # p_s5 = pygame.mixer.Sound('dnsehd.wav')
    #
    # p = pygame.mixer.Sound('1.wav')
    # p1 = pygame.mixer.Sound('2.wav')
    # p2 = pygame.mixer.Sound('3.wav')
    # p3 = pygame.mixer.Sound('4.wav')
    # p4 = pygame.mixer.Sound('5.wav')
    #
    # c_p = [p, p1, p2, p3, p4]

    # video read

    camera = cv2.VideoCapture(1)

    # Initiallization
    v_i = 2250
    s = 0
    squart_count = 0
    state = None
    # pi.set_servo_pulsewidth(17, 2500)
    # p_s.play()
    n = 1

    def left_calculate_angle(a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        left_c_angle = np.abs(radians * 180.0 / np.pi)

        if left_c_angle > 180.0:
            left_c_angle = 360 - left_c_angle

        return left_c_angle

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            success, frame = camera.read()  # read the camera frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False

            # Make detection
            results = pose.process(frame)

            # Recolor back to BGR
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates

                left_foot_index_x = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x]
                left_heel_x = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x]
                left_knee_x = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x]
                left_foot_index_y = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                left_knee_y = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                # if left_foot_index_y[0] < 0.9:
                #     motorL.forward(0.5)
                #     motorR.forward(0.5)
                # if left_foot_index_y[0] > 1:
                #     motorL.backward(0.5)
                #     motorR.backward(0.5)
                if 0.90 < left_foot_index_y[0] < 1:
                    #motorL.stop()
                    #motorR.stop()
                    if s == 0:
                        #p_s4.play()
                        # print(left_heel_x)
                        # print(left_foot_index_x)

                        s = 1
                        continue
                    else:
                        pass

                    if s == 1:
                        h_x = left_heel_x[0]
                        f_i_x = left_foot_index_x[0]
                        # print(h_x - f_i_x)
                        if (h_x - f_i_x) > 0.06:
                            #p_s5.play()
                            s = 2
                        # print(left_heel_x, left_foot_index_x)
                        pass
                # LEFT, RIGHT Calculate angle
                left_body_angle = left_calculate_angle(left_shoulder, left_hip, left_knee)
                left_leg_angle = left_calculate_angle(left_hip, left_knee, left_ankle)

                # cv2.putText(image, str(int(left_angle)),
                #            tuple(np.multiply(left_knee, [960, 240]).astype(int)),
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #            )
                if left_leg_angle > 160:
                    state = 'stand'
                if 90 < left_leg_angle < 110 and state == 'stand':
                    print(left_leg_angle)
                    state = 'squart'
                    squart_count += 1

                    m = left_knee_x[0] - left_foot_index_x[0]
                    if m < -0.02:
                        #p_s1.play()
                        squart_count -= 1
                    elif (left_body_angle < 80):
                        print(1, left_body_angle)
                        #p_s2.play()
                        squart_count -= 1
                    #else:
                        #c_p[squart_count - 1].play()
                print(left_leg_angle)
            except:
                print('출력안됨',file=sys.stderr)
            cv2.rectangle(frame, (0, 0), (225, 73), (255, 255, 255), -1)

            cv2.putText(frame, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(squart_count),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

            cv2.putText(frame, 'STATE', (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, state,
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )


            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index1.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    #app.run(debug=True)
    app.run(host='10.20.21.221', port="8080", debug=True)