# dashboard.py (Smart Learning Engagement Dashboard - Final Cloud Version)
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------- PAGE CONFIGURATION ----------------------
st.set_page_config(page_title="Smart Learning Engagement Dashboard", page_icon="📊", layout="wide")
st.title("📊 Smart Learning Engagement Dashboard")
st.caption("Visualize attention, focus, and emotions from recorded study sessions.")
st.markdown("---")

# ---------------------- FILE SELECTION ----------------------
st.sidebar.header("📂 Load Session Data")
uploaded_file = st.sidebar.file_uploader("Upload a session_log CSV", type=["csv"])

files_in_repo = [f for f in os.listdir() if f.startswith("session_log_") and f.endswith(".csv")]
selected_file = None
df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Uploaded file loaded successfully.")
elif files_in_repo:
    files_in_repo.sort(reverse=True)
    selected_file = st.sidebar.selectbox("Or choose a session file in repo", files_in_repo)
    if selected_file:
        df = pd.read_csv(selected_file)
else:
    st.warning("⚠️ No session logs found or uploaded. Run the local analyzer to create a 'session_log_*.csv' file, then upload it here.")
    st.stop()

# ---------------------- SESSION SUMMARY ----------------------
st.subheader("🧾 Session Summary")
st.write(f"Total frames recorded: **{len(df)}**")

avg_engagement = df["final_engagement"].mean()
avg_focus = df["focus_score"].mean()
avg_emotion_score = df["emotion_score"].mean()
top_emotion = df["emotion"].mode()[0] if not df["emotion"].mode().empty else "Unknown"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Engagement", f"{avg_engagement:.1f}%")
col2.metric("Average Focus", f"{avg_focus:.1f}%")
col3.metric("Emotion Score", f"{avg_emotion_score:.1f}%")
col4.metric("Most Common Emotion", top_emotion.title())

st.markdown("---")

# ---------------------- VISUALIZATIONS ----------------------
fig1 = px.line(df, x="timestamp", y="final_engagement", title="📈 Engagement Over Time", markers=True)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(df, x="timestamp", y=["focus_score", "emotion_score"], title="🎯 Focus vs Emotion Trends", markers=True)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(df, x="emotion", title="💭 Emotion Frequency", color="emotion")
st.plotly_chart(fig3, use_container_width=True)

# ---------------------- DOWNLOAD REPORT ----------------------
st.markdown("---")
session_summary_csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Engagement Report", data=session_summary_csv,
                   file_name="engagement_report.csv", mime="text/csv")

# ---------------------- ENGAGEMENT INTERPRETATION ----------------------
st.markdown("### 🧠 Engagement Analysis Summary")
if avg_engagement > 80:
    st.success("🌟 Excellent engagement! You maintained high focus throughout the session.")
elif avg_engagement > 60:
    st.info("🙂 Good engagement. You were mostly attentive with a few minor distractions.")
elif avg_engagement > 40:
    st.warning("😐 Moderate engagement. Some distraction or low attention periods detected.")
else:
    st.error("⚠️ Low engagement detected. Try improving your learning environment.")

# ---------------------- AI SUMMARY FEEDBACK ----------------------
st.markdown("---")
st.subheader("🤖 AI Summary Feedback")

if avg_focus > 80 and avg_emotion_score > 70:
    feedback = "Excellent performance! You maintained great focus and a positive emotional state throughout the session. Keep up the same energy!"
elif 60 <= avg_focus <= 80:
    feedback = "Good session overall. Focus was steady but there were short drops. Try short breaks every 30 minutes."
elif avg_emotion_score < 50:
    feedback = "Your emotional engagement seemed low. Try adding more interactive or fun learning materials to stay motivated."
else:
    feedback = "There’s room for improvement. Track when your focus drops and make changes to your study setup."

st.write(feedback)

# ---------------------- MULTI-SESSION TREND ----------------------
st.markdown("---")
st.subheader("📈 Multi-Session Performance Trend")

session_files = sorted(
    [f for f in os.listdir() if f.startswith("session_log_") and f.endswith(".csv")],
    reverse=False
)

if len(session_files) > 1:
    trend_data = []
    for f in session_files:
        try:
            temp_df = pd.read_csv(f)
            trend_data.append({
                "Session": f.replace("session_log_", "").replace(".csv", ""),
                "Engagement": temp_df["final_engagement"].mean(),
                "Focus": temp_df["focus_score"].mean(),
                "Emotion": temp_df["emotion_score"].mean()
            })
        except Exception as e:
            print(f"⚠️ Skipped {f}: {e}")

    trend_df = pd.DataFrame(trend_data)
    fig_trend = px.line(
        trend_df,
        x="Session",
        y=["Engagement", "Focus", "Emotion"],
        markers=True,
        title="📊 Engagement Progress Over Multiple Sessions"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("📅 Upload or record multiple sessions to view progress trends.")

# ---------------------- SMART AI RECOMMENDATIONS ----------------------
st.markdown("---")
st.subheader("🧠 Personalized AI Recommendations")

recommendations = []

if avg_engagement < 50:
    recommendations.append("⚠️ Engagement is quite low. Reduce distractions such as mobile phones or background noise.")
elif avg_engagement < 70:
    recommendations.append("🙂 Engagement is decent. Consider keeping study sessions shorter (20–30 minutes) to maintain focus.")
else:
    recommendations.append("🌟 Excellent engagement! Keep up your current study pattern and habits.")

if avg_focus < 50:
    recommendations.append("🎯 Focus is low. Try studying in a quiet, well-lit area and avoid multitasking.")
elif avg_focus < 70:
    recommendations.append("🧩 Medium focus. Include small breaks and try interactive learning tools like videos or quizzes.")
else:
    recommendations.append("🔥 Focus level is strong! You’re managing distractions effectively.")

if avg_emotion_score < 50:
    recommendations.append("💬 Emotion levels seem low. Do stress-relief activities like deep breathing before study sessions.")
elif top_emotion.lower() in ["sad", "angry", "tired"]:
    recommendations.append("😌 You seemed emotionally down. Take a short break or listen to relaxing music.")
else:
    recommendations.append("😊 Positive emotional state detected — a great mindset for learning!")

# Display recommendations neatly
for r in recommendations:
    st.markdown(r)

# ---------------------- END OF DASHBOARD ----------------------
st.markdown("---")
st.caption("Smart Learning Engagement Dashboard © 2025 | Developed by Anuska Gupta")
