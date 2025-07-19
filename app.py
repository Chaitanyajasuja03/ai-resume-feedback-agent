import streamlit as st
import PyPDF2
import io
from openai import OpenAI

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📄 AI Resume Feedback Agent")
st.write("Upload your resume and get instant feedback powered by OpenAI GPT!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

# Extract text from PDF
def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        return ""

# Analyze resume using OpenAI
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
        return f"Error: {str(e)}"

# Main App Logic
if uploaded_file is not None:
    resume_text = extract_text(uploaded_file)
    st.subheader("📃 Extracted Resume Text")
    with st.expander("Click to view"):
        st.write(resume_text)

    st.subheader("🔍 GPT Feedback")
    with st.spinner("Analyzing your resume..."):
        feedback = analyze_resume(resume_text)
        st.write(feedback)
