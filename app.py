import streamlit as st
from textblob import TextBlob
import speech_recognition as sr
import matplotlib.pyplot as plt

# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(page_title="🎤 AI Sentiment Analyzer", page_icon="😊", layout="wide")

# Custom CSS for dark theme + background styling
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .stTextArea textarea {
            background-color: #1e1e1e;
            color: #ffffff;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 8px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #45a049;
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Voice Input Function
# -------------------------------
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("⚠ API unavailable. Try again later.")
        except sr.WaitTimeoutError:
            st.warning("⌛ You took too long. Please try again.")
    return ""

# -------------------------------
# UI Layout
# -------------------------------
st.title("🎤 AI Sentiment Analyzer")
st.markdown("💬 Type or speak your thoughts, and let AI detect the mood instantly!")

# Initialize session state for storing input
if "manual_input" not in st.session_state:
    st.session_state.manual_input = ""

# Text area for manual input
st.markdown("### ✍ Enter Text or Use Voice")
text_area = st.text_area("Write your text here:", st.session_state.manual_input, height=100)

# Buttons in columns
col1, col2 = st.columns(2)

with col1:
    if st.button("🎤 Speak"):
        voice_text = get_voice_input()
        if voice_text:
            st.session_state.manual_input = voice_text
            st.experimental_rerun()

with col2:
    analyze_btn = st.button("🔍 Analyze Sentiment")

# -------------------------------
# Sentiment Analysis
# -------------------------------
if analyze_btn:
    text = text_area.strip() or st.session_state.get("manual_input", "")
    if text:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Display sentiment score
        st.success(f"*Sentiment Score (Polarity):* {sentiment:.2f}")
        st.info(f"*Subjectivity Score:* {subjectivity:.2f}")

        # Emoji feedback
        if sentiment > 0:
            st.markdown("### 😃 Positive Vibes!")
        elif sentiment < 0:
            st.markdown("### 😞 Negative Mood")
        else:
            st.markdown("### 😐 Neutral")

        # Chart visualization
        fig, ax = plt.subplots()
        ax.bar(["Polarity", "Subjectivity"], [sentiment, subjectivity], color=["skyblue", "orange"])
        ax.axhline(0, color="white", linewidth=1)
        ax.set_ylim(-1, 1)
        ax.set_facecolor("#1e1e1e")
        fig.patch.set_facecolor("#121212")
        st.pyplot(fig)

        # -------------------------------
        # Explanations
        # -------------------------------
        st.markdown("### 📘 What do these mean?")
        st.markdown("""
        - *Polarity: Ranges from **-1 (negative)* to *+1 (positive)*.  
          It tells if the text is emotionally negative, neutral, or positive.  
        - *Subjectivity: Ranges from **0 (objective/factual)* to *1 (subjective/opinionated)*.  
          It shows whether the text is more factual or personal in nature.
        """)
    else:
        st.warning("⚠ Please enter some text or use voice input first.")
