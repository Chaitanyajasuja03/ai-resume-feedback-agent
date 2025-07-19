import streamlit as st
import PyPDF2
import openai

st.set_page_config(page_title="AI Resume Feedback Agent")

# Load OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📄 AI Resume Feedback Agent")
st.markdown("Upload your resume and get instant feedback powered by **OpenAI GPT**!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    resume_text = ""

    if uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("📃 Extracted Resume Text")
    with st.expander("Click to view"):
        st.text_area("Resume Text", resume_text, height=300)

    st.subheader("🔍 GPT Feedback")
    with st.spinner("Analyzing resume..."):

        try:
            messages = [
                {"role": "system", "content": "You are a professional resume reviewer. Provide detailed, constructive feedback."},
                {"role": "user", "content": f"Please give me resume feedback for this:\n\n{resume_text}"}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            feedback = response.choices[0].message.content
            st.success("Resume analyzed successfully!")
            st.write(feedback)

        except openai.error.AuthenticationError:
            st.error("❌ Invalid OpenAI API Key. Please check your secrets.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
