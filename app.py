import streamlit as st
import dashboard

st.set_page_config(
    page_title="Smart Learning Engagement System",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Smart Learning Engagement System")
st.caption("Analyze student engagement using AI-based emotion, focus, and attention tracking.")

st.markdown("---")

st.markdown("""
### 📋 Choose a Module

📹 **Analyzer (Local Only)**  
Run real-time webcam engagement analysis locally on your computer.

📊 **Dashboard (Cloud Compatible)**  
Upload engagement session logs and view analytics.
""")

choice = st.radio("Select Module:", ["📹 Analyzer", "📊 Dashboard"])

# -------------------- ANALYZER --------------------

if choice == "📹 Analyzer":

    st.warning("⚠️ The Analyzer uses webcam and OpenCV, so it only runs locally.")

    st.markdown("""
### How to Run Analyzer Locally

1️⃣ Open terminal in your project folder.

2️⃣ Run:


3️⃣ This will generate a file like:

                
4️⃣ Upload that file in the **Dashboard section** to view analytics.
""")

# -------------------- DASHBOARD --------------------

elif choice == "📊 Dashboard":

    st.success("Opening Engagement Dashboard")

    dashboard.main()

st.markdown("---")
st.caption("Smart Learning Engagement System © 2025 | Developed by Anuska Gupta")