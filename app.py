import streamlit as st

st.markdown(
    '<meta name="google-site-verification" content="IH12TWW4S5y7HBJOp4GbhrDBPwylUE-jEglVe2NkgxM" />' ,
    unsafe_allow_html=True
    )

import speech_recognition as sr
import PyPDF2
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- VOICE INPUT FUNCTION ---
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak clearly into your microphone.")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio.")
    except sr.RequestError:
        st.error("❌ Speech Recognition API unavailable.")
    return ""

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="💭", layout="centered")

# --- HEADER ---
st.markdown("""
    <h1 style='text-align: center; color: #800080;'>💭 AI Sentiment Analyzer</h1>
    <p style='text-align: center; font-size: 18px;'>Analyze how positive, negative, or neutral your text is!</p>
""", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR ---
with st.sidebar:
    st.header("📘 About the App")
    st.markdown("This is a simple AI sentiment analyzer built using Python, Streamlit, and TextBlob.")
    st.markdown("Made with 💙 by Insanex467")

# --- LAYOUT ---
col1, col2 = st.columns([1, 2])
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062634.png", width=120, caption="Sentiment Icon")

with col2:
    st.subheader("📝 Enter your text below:")
    uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])

    # 1. FILE INPUT
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            st.session_state.text_input = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            st.session_state.text_input = text

    # 2. MANUAL TEXT AREA
    manual_input = st.text_area("Or enter text manually:", value=st.session_state.text_input, key="manual_input", height=150)

    # 3. VOICE INPUT
    if st.button("🎙 Use Voice Input"):
        voice_text = get_voice_input()
        if voice_text:
            st.session_state.text_input = voice_text
            st.rerun()  # rerun to update textarea with voice input

# --- SENTIMENT ANALYSIS ---
if st.button("🔍 Analyze Sentiment"):
    if not st.session_state.text_input.strip():
        st.warning("⚠ Please enter some text.")
    else:
        blob = TextBlob(st.session_state.text_input)
        polarity = blob.sentiment.polarity

        st.subheader("📈 Sentiment Analysis Result")
        if polarity > 0:
            st.markdown("<h3 style='color:green;'>🙂 Positive Sentiment</h3>", unsafe_allow_html=True)
        elif polarity < 0:
            st.markdown("<h3 style='color:red;'>☹ Negative Sentiment</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:gray;'>😐 Neutral Sentiment</h3>", unsafe_allow_html=True)

        # Bar chart
        fig, ax = plt.subplots()
        ax.bar("Sentiment", [polarity], color="skyblue")
        ax.set_ylim([-1, 1])
        ax.set_xlabel("Polarity Score (-1 to 1)")
        ax.axhline(0, color="black", linestyle="--")
        st.pyplot(fig)
