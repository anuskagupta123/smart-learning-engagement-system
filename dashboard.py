import streamlit as st
import pandas as pd
import plotly.express as px
import os

def main():

    st.set_page_config(
        page_title="Smart Learning Engagement Dashboard",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Smart Learning Engagement Dashboard")
    st.caption("Visualize attention, focus, and emotions from recorded study sessions.")
    st.markdown("---")

    # ---------------- FILE UPLOAD ----------------

    st.sidebar.header("📂 Load Session Data")

    uploaded_file = st.sidebar.file_uploader(
        "Upload a session_log CSV",
        type=["csv"]
    )

    df = None

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)
        st.sidebar.success("File uploaded successfully")

    else:
        st.warning("Upload a session_log CSV file to start analysis.")
        st.stop()

    # ---------------- SESSION SUMMARY ----------------

    st.subheader("🧾 Session Summary")

    avg_engagement = df["final_engagement"].mean()
    avg_focus = df["focus_score"].mean()
    avg_emotion_score = df["emotion_score"].mean()

    top_emotion = (
        df["emotion"].mode()[0]
        if not df["emotion"].mode().empty
        else "Unknown"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Engagement", f"{avg_engagement:.1f}%")
    col2.metric("Average Focus", f"{avg_focus:.1f}%")
    col3.metric("Emotion Score", f"{avg_emotion_score:.1f}%")
    col4.metric("Most Common Emotion", top_emotion.title())

    st.markdown("---")

    # ---------------- CHARTS ----------------

    fig1 = px.line(
        df,
        x="timestamp",
        y="final_engagement",
        title="📈 Engagement Over Time",
        markers=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        df,
        x="timestamp",
        y=["focus_score", "emotion_score"],
        title="🎯 Focus vs Emotion Trends",
        markers=True
    )

    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(
        df,
        x="emotion",
        title="💭 Emotion Frequency",
        color="emotion"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # ---------------- DOWNLOAD REPORT ----------------

    st.markdown("---")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Engagement Report",
        data=csv,
        file_name="engagement_report.csv",
        mime="text/csv"
    )

    # ---------------- ENGAGEMENT ANALYSIS ----------------

    st.markdown("### 🧠 Engagement Analysis Summary")

    if avg_engagement > 80:
        st.success("Excellent engagement throughout the session.")
    elif avg_engagement > 60:
        st.info("Good engagement with small drops in attention.")
    elif avg_engagement > 40:
        st.warning("Moderate engagement detected.")
    else:
        st.error("Low engagement detected.")

    # ---------------- AI FEEDBACK ----------------

    st.markdown("---")
    st.subheader("🤖 AI Feedback")

    if avg_focus > 80 and avg_emotion_score > 70:
        st.write("Excellent performance! You maintained strong focus and positive emotions.")
    elif avg_focus > 60:
        st.write("Good session overall. Consider short breaks to maintain attention.")
    else:
        st.write("Try improving your study environment to increase focus.")

    # ---------------- RECOMMENDATIONS ----------------

    st.markdown("---")
    st.subheader("🧠 Smart Recommendations")

    recommendations = []

    if avg_engagement < 50:
        recommendations.append("Reduce distractions such as phones or noise.")

    if avg_focus < 50:
        recommendations.append("Study in a quiet and well-lit environment.")

    if avg_emotion_score < 50:
        recommendations.append("Try relaxing before studying to improve emotional engagement.")

    if not recommendations:
        recommendations.append("Great job! Keep following your current study routine.")

    for r in recommendations:
        st.markdown(f"• {r}")

    st.markdown("---")
    st.caption("Smart Learning Engagement Dashboard © 2025 | Developed by Anuska Gupta")