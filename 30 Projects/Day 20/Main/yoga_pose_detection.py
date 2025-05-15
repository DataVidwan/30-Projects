import cv2
import mediapipe as mp
import math

# --- Function to calculate angle between 3 points ---
def calculate_angle(a, b, c):
    a = [a.x, a.y]
    b = [b.x, b.y]
    c = [c.x, c.y]

    ba = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]

    dot_product = ba[0]*bc[0] + ba[1]*bc[1]
    magnitude = math.sqrt(ba[0]**2 + ba[1]**2) * math.sqrt(bc[0]**2 + bc[1]**2)

    if magnitude == 0:
        return 0

    angle_rad = math.acos(dot_product / magnitude)
    angle_deg = math.degrees(angle_rad)

    return round(angle_deg, 2)

# Initialize MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 960)  # Height

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    pose_name = "Unknown Pose"

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get key joints
        l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        l_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        l_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        l_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        l_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        l_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

        r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        r_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        r_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        r_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Calculate angles
        left_elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        right_elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

        left_leg_angle = calculate_angle(l_hip, l_knee, l_ankle)
        right_leg_angle = calculate_angle(r_hip, r_knee, r_ankle)

        # ----- TADASANA -----
        if (170 < left_elbow_angle < 190 and
            170 < right_elbow_angle < 190 and
            l_wrist.y < l_shoulder.y and
            r_wrist.y < r_shoulder.y and
            170 < left_leg_angle < 190 and
            170 < right_leg_angle < 190):
            pose_name = "Tadasana (Mountain Pose)"

        # ----- VRIKSHASANA -----
        elif ((170 < left_leg_angle < 190 and right_leg_angle < 140) or
              (170 < right_leg_angle < 190 and left_leg_angle < 140)):
            pose_name = "Vrikshasana (Tree Pose)"

    # Display the pose name
    cv2.putText(frame, f'Pose: {pose_name}', (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    # Show the frame
    cv2.imshow('Yoga Pose Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
