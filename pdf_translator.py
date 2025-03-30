import streamlit as st
from io import BytesIO
from PIL import Image
import fitz  
from huggingface_hub import InferenceClient
import time

# Custom CSS styling
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

# Initialize Hugging Face client once
client = InferenceClient(
    model="deepseek-ai/DeepSeek-R1",
    api_key="Enter Huggingface Api-key Here"
)

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
bt = st.button("Translate")

def translate_text(text):
    """Handle translation with error handling and retries"""
    prompt = f"""### Instruction:
    Translate the following English text to fluent Persian while maintaining:
    - Technical terminology
    - Proper names
    - Numerical values
    - Formatting
    
    ### English Text:
    {text}
    
    ### Persian Translation:"""
    
    for _ in range(3):  # Retry up to 3 times
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=4000,
                temperature=0.3
            )
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            time.sleep(5)  # Wait before retrying
            
    return "Translation failed after multiple attempts"

if uploaded_file and bt:
    with st.spinner("Processing PDF..."):
        try:
            pdfdocument = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            full_translation = []
            
            for page_num in range(len(pdfdocument)):
                page = pdfdocument[page_num]
                text = page.get_text('text')
                
                if text.strip():
                    with st.expander(f"Page {page_num + 1} - Original Text"):
                        st.write(text)
                    
                    translated = translate_text(text)
                    full_translation.append(translated)
                    
                    with st.expander(f"Page {page_num + 1} - Translated Text", expanded=True):
                        st.markdown(translated)
                    
                    time.sleep(1)  # Rate limit protection
                
            # Show full translation
            st.success("Translation Complete!")
            st.download_button(
                label="Download Full Translation",
                data="\n\n".join(full_translation),
                file_name="translated_document.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"PDF Processing Error: {str(e)}")

# run translator with: streamlit run pdf_translator.py
