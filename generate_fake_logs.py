import os
import pandas as pd
import random
from datetime import datetime, timedelta

# Path to your extracted dataset folder
train_dir = "train"  # same as your folder name in Learning_Analyzer

# Emotion folders (e.g., happy, sad, angry, etc.)
emotions = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]

# Generate fake engagement and focus data for each image
data = []
timestamp = datetime.now()

for emotion in emotions:
    emotion_dir = os.path.join(train_dir, emotion)
    image_files = [f for f in os.listdir(emotion_dir) if f.endswith(".jpg") or f.endswith(".png")]

    for img in image_files:
        # Simulate frame data (you can modify ranges to make it more realistic)
        final_engagement = random.uniform(40, 95)
        focus_score = random.uniform(30, 100)
        emotion_score = random.uniform(40, 90)
        timestamp += timedelta(seconds=2)

        data.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "emotion": emotion,
            "final_engagement": round(final_engagement, 2),
            "focus_score": round(focus_score, 2),
            "emotion_score": round(emotion_score, 2)
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV file
output_file = f"session_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(output_file, index=False)

print(f"✅ Fake session log generated successfully: {output_file}")
print(f"Total frames simulated: {len(df)}")
print(f"Emotions included: {', '.join(emotions)}")
