# app.py (Main Entry - Smart Learning Engagement System)
import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Smart Learning Engagement System", page_icon="🧠", layout="centered")

st.title("🧠 Smart Learning Engagement System")
st.caption("Analyze student engagement using AI-based emotion, focus, and attention tracking.")

st.markdown("---")

st.markdown("""
### 📋 Choose a Module
Select whether you want to **analyze a learning session** or **view engagement dashboards**.

- **📹 Analyzer:** Run real-time or recorded video analysis to generate engagement logs.  
- **📊 Dashboard:** View visual analytics of engagement, emotion, and focus trends.
""")

choice = st.radio("Select Module:", ["📹 Analyzer", "📊 Dashboard"])

# -------------------- RUN MODULE --------------------
if choice == "📹 Analyzer":
    st.markdown("### 🎥 Running the Analyzer")
    st.info("This will start your webcam or process a pre-recorded session.")
    st.write("Make sure your camera and microphone are enabled.")

    if st.button("▶️ Launch Analyzer"):
        st.success("Launching analyzer... (this may take a few seconds)")
        subprocess.run(["python", "engagement_analyzer.py"])

elif choice == "📊 Dashboard":
    st.markdown("### 📊 Launching Dashboard")
    st.info("You can view and compare multiple engagement session reports.")

    if st.button("🚀 Open Dashboard"):
        st.success("Opening Smart Dashboard...")
        subprocess.run(["streamlit", "run", "dashboard.py"])

st.markdown("---")
st.caption("Smart Learning Engagement System © 2025 | Developed by Anuska Gupta")
