import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🧠",
    layout="centered"
)

# App Header
st.markdown("""
    <h1 style='text-align: center; color: #4B0082;'>🧠 AI Sentiment Analyzer</h1>
    <p style='text-align: center; font-size: 18px;'>Analyze how positive, negative, or neutral your text is!</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar Info
with st.sidebar:
    st.header("📘 About the App")
    st.markdown("This is a simple AI sentiment analyzer built using Python, Streamlit, and TextBlob.")
    st.markdown("Made with ❤ by Insanex467")

# Layout using columns
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062634.png", width=120, caption="Sentiment Icon")

with col2:
    st.subheader("Enter your text below:")
    text_input = st.text_area("Write something...", height=150)

if st.button("Analyze Sentiment"):
    if not text_input.strip():
        st.warning("⚠ Please enter some text.")
    else:
        blob = TextBlob(text_input)
        polarity = blob.sentiment.polarity

        st.subheader("📊 Sentiment Analysis Result")

        if polarity > 0:
            st.success("😊 Positive Sentiment")
        elif polarity < 0:
            st.error("😞 Negative Sentiment")
        else:
            st.info("😐 Neutral Sentiment")

        # Show polarity bar chart
        fig, ax = plt.subplots()
        ax.barh(['Sentiment'], [polarity], color='skyblue')
        ax.set_xlim(-1, 1)
        ax.set_xlabel("Polarity Score (-1 to 1)")
        ax.axvline(0, color='black', linestyle='--')
        st.pyplot(fig)
