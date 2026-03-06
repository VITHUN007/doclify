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

st.markdown("### Upload your project files (Python, JS, Java, etc.):")
uploaded_files = st.file_uploader(
    "Choose files", 
    accept_multiple_files=True,
    type=["py", "js", "java", "cpp", "cs", "go", "rb", "ts", "php", "html", "css", "json", "yaml", "md", "xml", "sh", "bat"],
    help="Upload your source code.files. Binary files are not supported."
)
if st.button("Generate README"):
    if not uploaded_files:
        st.warning("Please upload at least one file first!")
    else:
        with st.spinner("Analyzing code structure..."):
            full_context = ""
            file_summary = []

            for uploaded_file in uploaded_files:
                try:
                    file_bytes = uploaded_file.read()
                    content = file_bytes.decode("utf-8", errors="replace")
                    
                    full_context += f"\n\n--- START FILE: {uploaded_file.name} ---\n{content}\n--- END FILE: {uploaded_file.name} ---"
                    file_summary.append(uploaded_file.name)
                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {e}")

        
            prompt = (
                "Act as a Senior Software Architect. Below is a collection of source files from a project. "
                "1. Analyze the logic and purpose of the code.\n"
                "2. Create a high-quality GitHub README.md.\n"
                "3. Include: Project Title, Description, a 'Project Structure' tree, Installation, Usage, and Features.\n"
                "4. Be concise, professional, and use proper Markdown formatting.\n\n"
                f"PROJECT FILES:\n{full_context}"
            )

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt
                )

                st.success("Documentation Ready!")
                
                st.markdown("---")
                st.markdown("## Generated README.md")
                st.code(response.text, language="markdown")

                st.download_button(
                    label="Download README.md",
                    data=response.text,
                    file_name="README.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Gemini API Error: {e}")

if uploaded_files:
    st.info(f"Files that are uploaded for processing: {', '.join([f.name for f in uploaded_files])}")