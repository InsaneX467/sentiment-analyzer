import streamlit as st
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- Page Config ---
st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="💬", layout="centered")

# --- App Title ---
st.title("🎙 AI Sentiment Analyzer")
st.write("Analyze *text or voice input* and discover its sentiment instantly.")

# --- Initialize Recognizer & Analyzer ---
recognizer = sr.Recognizer()
analyzer = SentimentIntensityAnalyzer()

# --- Sidebar Info ---
with st.sidebar:
    st.header("ℹ About")
    st.write("This app uses *VADER Sentiment Analysis*, which is great for social media, casual texts, and voice input.")
    st.write("It gives scores for *Positive, Neutral, Negative* and an overall *Compound Sentiment*.")

# --- Text / Voice Input ---
st.subheader("📝 Enter Text or Use Voice")
text_input = st.text_area("Enter your text here:", height=150, placeholder="Type something or use voice...")

if st.button("🎤 Use Voice Input"):
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            text_input = recognizer.recognize_google(audio)
            st.success(f"Voice captured: {text_input}")
            st.session_state["text_input"] = text_input
        except Exception as e:
            st.error(f"Error: {e}")

# --- Sentiment Analysis ---
if st.button("🔎 Analyze Sentiment"):
    if text_input:
        scores = analyzer.polarity_scores(text_input)
        compound = scores['compound']
        pos, neu, neg = scores['pos'], scores['neu'], scores['neg']

        # Decide sentiment label
        if compound >= 0.05:
            sentiment = "Positive 😃"
        elif compound <= -0.05:
            sentiment = "Negative 😞"
        else:
            sentiment = "Neutral 😐"

        # --- Results ---
        st.markdown("## 📊 Results")
        st.success(f"*Overall Sentiment:* {sentiment}")
        st.write(f"*Positive Score:* {pos:.2f}")
        st.write(f"*Neutral Score:* {neu:.2f}")
        st.write(f"*Negative Score:* {neg:.2f}")
        st.write(f"*Compound Score:* {compound:.2f}")

        # --- Explanation ---
        st.markdown("---")
        st.markdown("### 📖 What the Scores Mean")
        st.write("- *Positive/Neutral/Negative:* Probability of each tone in the text.")
        st.write("- *Compound Score:* Overall sentiment, from -1 (most negative) to +1 (most positive).")
    else:
        st.warning("⚠ Please enter some text or use voice input.")s
