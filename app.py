import streamlit as st
from textblob import TextBlob
import speech_recognition as sr
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="📩")

st.title("📩 AI Sentiment Analyzer")
st.write("Upload a file, enter text, or use your voice to analyze sentiment.")

# File upload (TXT + PDF)
uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])

# Text input with session state
text = st.text_area("Or enter text manually:", key="manual_text")

# Voice input button
if st.button("🎙 Use Voice Input"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak now!")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    try:
        voice_text = recognizer.recognize_google(audio)
        st.session_state.manual_text = voice_text
        st.success(f"Voice captured: {voice_text}")
    except Exception as e:
        st.error(f"Voice input error: {e}")

# Analyze button
if st.button("🔍 Analyze Sentiment"):
    text_to_analyze = ""

    # If user uploaded file
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text_to_analyze = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text_to_analyze += page.extract_text()

    else:
        text_to_analyze = st.session_state.manual_text.strip()

    if not text_to_analyze:
        st.warning("⚠ Please provide text via upload, typing, or voice.")
    else:
        # Sentiment analysis
        blob = TextBlob(text_to_analyze)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        st.subheader("📊 Sentiment Results")
        if polarity > 0:
            st.success("😊 Positive Sentiment")
        elif polarity < 0:
            st.error("☹ Negative Sentiment")
        else:
            st.info("😐 Neutral Sentiment")

        st.write(f"*Polarity:* {polarity:.2f}")
        st.write(f"*Subjectivity:* {subjectivity:.2f}")

        # Bar chart visualization
        st.subheader("📈 Visualization")
        fig, ax = plt.subplots()
        ax.bar(["Polarity", "Subjectivity"], [polarity, subjectivity])
        ax.set_ylim(-1, 1)
        ax.set_ylabel("Score")
        st.pyplot(fig)
