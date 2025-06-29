import streamlit as st
from textblob import TextBlob
import pandas as pd
import re

st.set_page_config(page_title="Sentiment Analyzer", layout="centered")

# --- Preprocessing function ---
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # remove special chars/emojis
    text = text.strip()
    return text

# --- App title ---
st.title("🧠 Sentiment Analyzer")
st.write("Analyze your text sentiment with feedback, score, and export option.")

# --- User input ---
user_input = st.text_area("Enter text here:")

if user_input:
    cleaned_text = clean_text(user_input)
    analysis = TextBlob(cleaned_text)
    score = analysis.sentiment.polarity

    # --- Display sentiment score ---
    st.markdown(f"### Sentiment Score: {score:.2f}")

    # --- Emoji / confidence feedback ---
    if score > 0.5:
        st.success("😊 Very Positive")
    elif score > 0:
        st.info("🙂 Slightly Positive")
    elif score == 0:
        st.warning("😐 Neutral")
    elif score > -0.5:
        st.warning("🙁 Slightly Negative")
    else:
        st.error("😡 Very Negative")

    # --- Optional export ---
    df = pd.DataFrame({"Text": [cleaned_text], "Score": [score]})
    csv = df.to_csv(index=False)
    st.download_button("📥 Download Result as CSV", csv, "sentiment_result.csv", "text/csv")
