import streamlit as st
from textblob import TextBlob
import speech_recognition as sr
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Sentiment Analyzer", layout="centered")

st.title("🧠 AI Sentiment Analyzer")
st.write("Analyze sentiment from text input or your voice.")

# --- Voice Input Function ---
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... please speak clearly.")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand the audio.")
        return ""
    except sr.RequestError:
        st.error("Could not connect to the recognition service.")
        return ""

# --- Session State Setup ---
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""

# --- Input Options ---
manual_text = st.text_area("✍ Enter text manually:", key="manual_input")

if st.button("🎤 Record Voice"):
    st.session_state.voice_input = record_voice()

voice_text = st.session_state.voice_input
if voice_text:
    st.info(f"🎤 Voice Input: {voice_text}")

# --- Analyze Sentiment ---
if st.button("🔍 Analyze Sentiment"):
    text_to_analyze = manual_text or voice_text  # Use whichever is available

    if not text_to_analyze.strip():
        st.warning("⚠ Please enter or record some text before analyzing.")
    else:
        analysis = TextBlob(text_to_analyze)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        st.subheader("📊 Sentiment Analysis Result")
        if polarity > 0:
            st.success("Positive 😊")
        elif polarity < 0:
            st.error("Negative 😠")
        else:
            st.info("Neutral 😐")

        # Display metrics
        col1, col2 = st.columns(2)
        col1.metric("Polarity", f"{polarity:.2f}")
        col2.metric("Subjectivity", f"{subjectivity:.2f}")

        # --- Visualization ---
        fig, ax = plt.subplots()
        labels = ["Polarity", "Subjectivity"]
        values = [polarity, subjectivity]
        ax.bar(labels, values)
        ax.set_ylim(-1, 1)
        ax.set_title("Sentiment Metrics")
        st.pyplot(fig)
