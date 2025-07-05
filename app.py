import streamlit as st
from textblob import TextBlob

# Page config
st.set_page_config(page_title="Sentiment Analyzer", page_icon="💬")

# Title
st.title("🧠 AI Sentiment Analyzer")

# Text input
st.subheader("Enter your text below:")
text_input = st.text_area("Write something...", "")

# Analyze button
if st.button("Analyze Sentiment"):
    if text_input.strip() != "":
        blob = TextBlob(text_input)
        sentiment = blob.sentiment.polarity

        st.subheader("Sentiment Analysis Result:")
        if sentiment > 0:
            st.success("Positive 😊")
        elif sentiment < 0:
            st.error("Negative 😠")
        else:
            st.info("Neutral 😐")
    else:
        st.warning("Please enter some text.")
