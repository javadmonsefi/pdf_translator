### install needed libraries
# pip install streamlit
# pip install PyMuPDf
# pip install fitz
# pip install openai
# pip install huggingface_hub
# ------------------------------------------------------------------------------------

import streamlit as st
from io import BytesIO
from PIL import Image
import fitz  # PyMuPDf
from openai import OpenAI
from huggingface_hub import InferenceClient

client = OpenAI(api_key="???")   # set your OpenAI API key

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,500&family=Noto+Sans+Arabic:wght@500&display=swap');
html { direction: rtl; }
.st-emotion-cache-1fttcpj, .st-emotion-cache-nwtri { display: none; }
.st-emotion-cache-5rimss p { text-align: right; font-family: 'DM Sans', sans-serif; }
pre { text-align: left; }
h1, h2, h3, h4, h5, h6 { font-family: 'Noto Sans Arabic', sans-serif; }
span, p, a, button, ol, li { text-align: right; font-family: 'DM Sans', sans-serif; }
</style>
""", unsafe_allow_html=True)

st.title('PDF Translator')

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

bt = st.button("Translate")

if uploaded_file and bt:
    pdfdocument = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page_num in range(len(pdfdocument)):
        page = pdfdocument[page_num]
        text = page.get_text('text')
        translate = client.chat.completions.create(
            model='gpt-4o-mini',  # set the model
            messages=[
                {
                    'role': 'system', 
                    'content': 'translate all texts into fluent persian'
                },
                {
                    'role': 'user', 
                    'content': text
                }
            ]
        )

    st.markdown(translate.choices[0].message.content)

    # time.sleep(3)  # Optional: Add a delay to manage rate limit

# ------------------------------------------------------------------------------------
# run with this command:
# streamlit run translator_OpenAI.py
