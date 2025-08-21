import streamlit as st
from textblob import TextBlob
import speech_recognition as sr
import matplotlib.pyplot as plt

# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(page_title="🎤 AI Sentiment Analyzer", page_icon="😊", layout="wide")

# Custom CSS for modern UI
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
            color: #333333;
        }
        .stTextArea textarea {
            background-color: #ffffff !important;
            color: #333333 !important;
            border: 1px solid #dcdcdc;
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
        }
        .stButton>button {
            background: linear-gradient(90deg, #4facfe, #00f2fe);
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #00f2fe, #4facfe);
            transform: scale(1.05);
        }
        .result-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }
        .emoji {
            font-size: 40px;
            text-align: center;
            margin-bottom: 10px;
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
text_area = st.text_area("✍ Enter your text here:", st.session_state.manual_input, height=100)

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

        # Result card
        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        # Emoji feedback
        if sentiment > 0:
            st.markdown('<div class="emoji">😃</div>', unsafe_allow_html=True)
            st.markdown("### Positive Vibes!")
        elif sentiment < 0:
            st.markdown('<div class="emoji">😞</div>', unsafe_allow_html=True)
            st.markdown("### Negative Mood")
        else:
            st.markdown('<div class="emoji">😐</div>', unsafe_allow_html=True)
            st.markdown("### Neutral")

        st.success(f"*Sentiment Score (Polarity):* {sentiment:.2f}")
        st.info(f"*Subjectivity Score:* {subjectivity:.2f}")

        # Chart visualization
        fig, ax = plt.subplots()
        ax.bar(["Polarity", "Subjectivity"], [sentiment, subjectivity], color=["#4facfe", "#ffb347"])
        ax.axhline(0, color="gray", linewidth=1)
        ax.set_ylim(-1, 1)
        st.pyplot(fig)

        # Definitions
        st.markdown("### 📘 What do these mean?")
        st.markdown("""
        - *Polarity: Ranges from **-1 (negative)* to *+1 (positive)*.  
          It tells if the text is emotionally negative, neutral, or positive.  
        - *Subjectivity: Ranges from **0 (objective/factual)* to *1 (subjective/opinionated)*.  
          It shows whether the text is more factual or personal in nature.
        """)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠ Please enter some text or use voice input first.")
