import streamlit as st
from openai import OpenAI
import PyPDF2

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume reviewer."},
                {"role": "user", "content": f"Please review this resume and provide detailed feedback:\n\n{resume_text}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error analyzing resume:\n\n{e}"
