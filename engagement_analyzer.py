import cv2
import mediapipe as mp
from deepface import DeepFace
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime

# === Initialization ===
mp_face = mp.solutions.face_detection
mp_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not detected!")
    exit()

face_detector = mp_face.FaceDetection(min_detection_confidence=0.5)
face_mesh = mp_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

# === Live graph setup ===
plt.ion()
fig, ax = plt.subplots()
engagement_values = deque(maxlen=50)
line, = ax.plot([], [], 'g-', linewidth=2)
ax.set_ylim(0, 100)
ax.set_xlim(0, 50)
ax.set_xlabel('Time (frames)')
ax.set_ylabel('Engagement (%)')
ax.set_title('📊 Real-Time Engagement Trend')

# === Create CSV log file ===
session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"session_log_{session_id}.csv"
log_data = []

print(f"🧾 Logging session data to {log_filename}")

def get_focus_score(landmarks, w, h):
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    left_eye = np.array([int(left_eye.x * w), int(left_eye.y * h)])
    right_eye = np.array([int(right_eye.x * w), int(right_eye.y * h)])
    face_center = (left_eye + right_eye) // 2
    frame_center = np.array([w // 2, h // 2])
    dist = np.linalg.norm(face_center - frame_center)
    max_dist = w / 3
    return int(max(0, 100 - (dist / max_dist * 100)))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape
    results = face_detector.process(rgb)
    mesh_results = face_mesh.process(rgb)

    emotion_score = 50
    focus_score = 50
    dominant_emotion = "unknown"

    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            x, y, bw, bh = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
            face_crop = frame[y:y+bh, x:x+bw]

            try:
                analysis = DeepFace.analyze(face_crop, actions=['emotion'], enforce_detection=False)
                dominant_emotion = analysis[0]['dominant_emotion']
                emotion_score = {
                    "happy": 100, "surprise": 85, "neutral": 70,
                    "sad": 40, "angry": 30, "fear": 25, "disgust": 15
                }.get(dominant_emotion, 50)
            except:
                pass

            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
            cv2.putText(frame, f"{dominant_emotion.upper()} ({emotion_score}%)", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    if mesh_results.multi_face_landmarks:
        for face_landmarks in mesh_results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            focus_score = get_focus_score(landmarks, w, h)

    final_score = int((emotion_score + focus_score) / 2)

    # === Live graph update ===
    engagement_values.append(final_score)
    line.set_ydata(list(engagement_values))
    line.set_xdata(np.arange(len(engagement_values)))
    ax.set_xlim(max(0, len(engagement_values) - 50), len(engagement_values))
    ax.figure.canvas.draw()
    ax.figure.canvas.flush_events()

    # === Engagement bar on video ===
    bar_len = int(final_score * 3)
    cv2.rectangle(frame, (30, 30), (30 + bar_len, 60), (0, 255, 0), -1)
    cv2.putText(frame, f"Engagement: {final_score}%", (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("📸 Smart Engagement Analyzer", frame)

    # === Log data each frame ===
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_data.append({
        "timestamp": timestamp,
        "emotion": dominant_emotion,
        "emotion_score": emotion_score,
        "focus_score": focus_score,
        "final_engagement": final_score
    })

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Save log on exit ===
cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()

df = pd.DataFrame(log_data)
df.to_csv(log_filename, index=False)
print(f"✅ Session log saved: {log_filename}")
