import streamlit as st
import PyPDF2
import openai
import os

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="📄 AI Resume Feedback Agent")

st.title("📄 AI Resume Feedback Agent")
st.write("Upload your resume and get instant feedback powered by OpenAI GPT!")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    else:
        return ""

def analyze_resume(text):
    try:
        prompt = (
            "You are a professional career coach. Review the following resume and provide constructive feedback, "
            "highlight strengths, weaknesses, and suggestions for improvement:\n\n"
            f"{text}"
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI career assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error analyzing resume: {str(e)}"

# Main logic
if uploaded_file is not None:
    st.success(f"Uploaded File: {uploaded_file.name}")

    resume_text = extract_text(uploaded_file)

    if resume_text:
        with st.expander("📃 Extracted Resume Text"):
            st.write(resume_text)

        with st.spinner("Analyzing with GPT..."):
            feedback = analyze_resume(resume_text)

        st.subheader("🔍 GPT Feedback")
        st.write(feedback)
    else:
        st.error("Couldn't extract any text from the file.")
