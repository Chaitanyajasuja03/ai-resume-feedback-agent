import streamlit as st
import PyPDF2
import openai

# Load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define function to analyze resume
def analyze_resume(resume_text):
    prompt = f"""
You are an expert career coach. A user has uploaded the following resume:

\"\"\"{resume_text}\"\"\"

Please give detailed feedback including:
1. Resume structure and formatting
2. Grammar or clarity issues
3. Missing sections (e.g., summary, skills, etc.)
4. How well it matches general industry standards
5. Suggestions for improvement

Respond professionally and helpfully.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume analyzer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error analyzing resume: {e}"

# Streamlit app UI
st.title("📄 AI Resume Feedback Agent")
st.write("Upload your resume and get instant feedback powered by GPT!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file is not None:
    st.success(f"Uploaded File: {uploaded_file.name}")

    # Extract text
    resume_text = ""
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("📃 Extracted Resume Text")
    with st.expander("Click to view"):
        st.text_area("Resume Text", resume_text, height=300)

    st.subheader("🔍 GPT Feedback")
    feedback = analyze_resume(resume_text)
    st.write(feedback)
