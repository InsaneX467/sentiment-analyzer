import streamlit as st
import speech_recognition as sr
from textblob import TextBlob

st.set_page_config(page_title="Sentiment Analyzer", page_icon=":smile:")
st.title("🧠 AI Sentiment Analyzer")

# Function to get voice input
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            text = "Could not understand audio"
        except sr.RequestError:
            text = "Could not request results"
    return text

# Text input field
txt_input = st.text_area("Enter your text here or use voice input:", "")

# Voice input button
if st.button("🎙 Use Voice Input"):
    voice_text = get_voice_input()
    if voice_text:
        txt_input = voice_text
        st.success(f"Recognized Voice Input: {voice_text}")

# Analyze sentiment
if st.button("🔍 Analyze"):
    if txt_input.strip() != "":
        blob = TextBlob(txt_input)
        sentiment = blob.sentiment.polarity

        st.subheader("Sentiment Analysis Result")
        if sentiment > 0:
            st.success("😊 Positive Sentiment")
        elif sentiment < 0:
            st.error("😞 Negative Sentiment")
        else:
            st.info("😐 Neutral Sentiment")

        st.write(f"*Sentiment Score:* {sentiment}")
    else:
        st.warning("Please enter some text to analyze.")
