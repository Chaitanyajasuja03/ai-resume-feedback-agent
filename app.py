import streamlit as st
import PyPDF2
import io
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Resume analyzer function using the new OpenAI API format
def analyze_resume(resume_text):
    prompt = f"""
    You are a professional career coach and resume expert. Please review the following resume and provide constructive feedback.
    
    Resume:
    {resume_text}

    Please include:
    - Strengths in the resume
    - Weaknesses or areas for improvement
    - Suggestions for formatting or wording
    - Overall impression and rating out of 10
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume analyzer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing resume:\n\n{e}"

# Streamlit app
st.title("📄 AI Resume Feedback Agent")
st.write("Upload your resume and get instant feedback powered by GPT!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    st.write(f"Uploaded File: {uploaded_file.name}")

    # Extract text from uploaded file
    resume_text = ""
    if uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    elif uploaded_file.name.endswith(".txt"):
        resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("📃 Extracted Resume Text")
    with st.expander("Click to view"):
        st.text(resume_text)

    # Analyze resume
    st.subheader("🔍 GPT Feedback")
    with st.spinner("Analyzing your resume..."):
        feedback = analyze_resume(resume_text)
        st.write(feedback)
