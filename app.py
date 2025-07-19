import streamlit as st
import PyPDF2
import requests
import io

# Hugging Face model API
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
}

# Resume analyzer using Hugging Face LLM
def analyze_resume(resume_text):
    prompt = f"""
You are an expert resume reviewer. Give detailed feedback on the following resume:

\"\"\"{resume_text}\"\"\"

Feedback must include:
1. Structure and formatting
2. Grammar and clarity
3. Missing key sections
4. Relevance to tech/AI industry
5. Suggestions for improvement
"""

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 512}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error analyzing resume:\n\n{response.status_code} - {response.json()}"

# Streamlit app UI
st.title("📄 AI Resume Feedback Agent")
st.write("Upload your resume and get instant feedback powered by Hugging Face LLM!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    st.success(f"Uploaded File: {uploaded_file.name}")

    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text()
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("📃 Extracted Resume Text")
    with st.expander("Click to view"):
        st.text(resume_text)

    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing with Hugging Face LLM..."):
            feedback = analyze_resume(resume_text)
        st.subheader("🔍 GPT Feedback")
        st.write(feedback)
