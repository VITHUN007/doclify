import os
from dotenv import load_dotenv
import streamlit as st
from google import genai 

st.set_page_config(page_title="Doclify")

st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #f4f7f6;
    }
    
    /* Center the title and subtitle */
    .title-text {
        text-align: center;
        color: #0E1117;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Style the sidebar and inputs */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        font-family: 'Courier New', monospace;
    }
    
    /* Button styling */
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #FF2B2B;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

API_KEY = st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found!.")
    st.stop()
client = genai.Client(api_key=API_KEY)

st.markdown("<h1 class='title-text'> Doclify: AI README Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Paste your code and get the documentation.</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### Paste your code below:")

code_input = st.text_area(
    "Paste Code Here",
    height=300,
    placeholder="Copy and paste your Python/Java/HTML project code here..."
)

if st.button("Generate README"):
    if not code_input.strip():
        st.warning("Please paste some code first!")
    else:
        with st.spinner("Gemini is writing your README..."):
            prompt = f"You are a Senior Developer. Generate a professional GitHub README.md for the following code: {code_input}"

            response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
        )

        st.success("README Generated Successfully ")
        st.markdown("## Generated README.md")
        st.code(response.text, language="markdown")

        st.download_button(
            "⬇ Download README.md",
            response.text,
            file_name="README.md"
        )

