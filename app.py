import streamlit as st
from textblob import TextBlob
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

st.set_page_config(page_title="AI Sentiment Analyzer", layout="centered")

st.title("🎤 AI Sentiment Analyzer")
st.write("Analyze sentiment from *typed text* or *voice input*.")

# --- Input section ---
st.subheader("Enter Text or Use Voice Input")

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("Your text here:", key="manual_input", height=120)

with col2:
    if st.button("🎙 Speak"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... please speak")
            audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            voice_text = recognizer.recognize_google(audio)
            st.success(f"Voice captured: {voice_text}")
            user_input = voice_text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.error("Speech Recognition service error.")

# --- Sentiment Analysis ---
if st.button("🔎 Analyze Sentiment"):
    if user_input.strip() == "":
        st.warning("⚠ Please enter some text or use voice input.")
    else:
        # TextBlob analysis
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # VADER analysis
        vader_scores = analyzer.polarity_scores(user_input)
        vader_compound = vader_scores['compound']

        # Final sentiment decision (weighted combo)
        if vader_compound >= 0.05:
            sentiment = "😊 Positive"
        elif vader_compound <= -0.05:
            sentiment = "😞 Negative"
        else:
            sentiment = "😐 Neutral"

        # --- Results ---
        st.subheader("📊 Sentiment Results")
        st.markdown(f"*Overall Sentiment:* {sentiment}")
        st.markdown(f"*Polarity (TextBlob):* {polarity:.2f}")
        st.markdown(f"*Subjectivity (TextBlob):* {subjectivity:.2f}")
        st.markdown(f"*VADER Compound Score:* {vader_compound:.2f}")

        # Extra definitions
        with st.expander("ℹ Learn about Polarity & Subjectivity"):
            st.markdown("""
            - *Polarity* ranges from -1.0 (very negative) to +1.0 (very positive).  
            - *Subjectivity* ranges from 0.0 (very objective) to 1.0 (very subjective).  
            - *VADER Compound Score* combines multiple sentiment signals into a value between -1 (negative) and +1 (positive).
            """)
