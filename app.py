import streamlit as st
from resume_analyzer import analyze_resume
from utils import extract_text_from_pdf, extract_text_from_txt

st.set_page_config(page_title="AI Resume Feedback Agent", layout="centered")

st.title("📄 AI Resume Feedback Agent")
st.write("Upload your resume and get instant feedback powered by GPT!")

st.write("✅ Secrets loaded:", "OPENAI_API_KEY" in st.secrets)  # 👈 shows True/False
st.write("✅ API Key Test", st.secrets["OPENAI_API_KEY"][:5] + "..." + st.secrets["OPENAI_API_KEY"][-5:])


uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "txt":
        resume_text = extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    st.subheader("📃 Extracted Resume Text")
    with st.expander("Click to view"):
        st.text(resume_text[:3000])

    st.subheader("🔍 GPT Feedback")
    with st.spinner("Analyzing your resume..."):
        feedback = analyze_resume(resume_text)  # 👈 OpenAI call here

    st.success("Analysis complete!")
    st.markdown(feedback)
