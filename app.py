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
Run webcam engagement analysis locally on your computer.

📊 **Dashboard (Cloud Supported)**  
Upload engagement logs and view analytics.
""")

choice = st.radio("Select Module:", ["📹 Analyzer", "📊 Dashboard"])

# -------- ANALYZER --------

if choice == "📹 Analyzer":

    st.warning("⚠️ The analyzer uses webcam and cannot run on Streamlit Cloud.")

    st.markdown("""
### Run Analyzer Locally

Run this command on your computer:

It will generate:

Upload that file in the **Dashboard section**.
""")

# -------- DASHBOARD --------

elif choice == "📊 Dashboard":

    dashboard.main()

st.markdown("---")
st.caption("Smart Learning Engagement System © 2025 | Developed by Anuska Gupta")