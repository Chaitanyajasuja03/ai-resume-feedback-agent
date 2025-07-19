import streamlit as st
import PyPDF2
import io

st.set_page_config(page_title="📄 AI Resume Feedback Agent")

st.title("📄 AI Resume Feedback Agent")
st.markdown("Upload your resume and get instant feedback powered by GPT!")

# --- Upload Resume ---
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

resume_text = ""

if uploaded_file:
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
    st.write(f"**Uploaded File:** {file_details['filename']}")

    # --- Extract Text from PDF or TXT ---
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    elif uploaded_file.type == "text/plain":
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        resume_text = stringio.read()
    else:
        st.error("Unsupported file format.")
        st.stop()

    # --- Display Extracted Text ---
    with st.expander("📃 Extracted Resume Text"):
        st.write(resume_text)

    # --- Analyze Resume (Mock GPT Response) ---
    with st.spinner("Analyzing your resume..."):
        feedback = analyze_resume(resume_text)

    # --- Display Feedback ---
    st.subheader("🔍 GPT Feedback")
    st.markdown(feedback)

# --- Fake AI Resume Feedback Function ---
def analyze_resume(resume_text):
    return f"""
✅ **Resume Feedback**

**1. Structure & Formatting:**
The resume is well-organized, but ensure consistent font size and bullet formatting throughout.

**2. Grammar or Clarity Issues:**
Minor issues found with punctuation and verb tense. Be consistent with past/present tense based on job dates.

**3. Missing Sections:**
Include a **Professional Summary** at the top and a dedicated **Skills** section for quick scanning by recruiters.

**4. Industry Standard Match:**
The resume is mostly aligned with industry expectations for freshers. Highlighting key achievements in projects would improve visibility.

**5. Suggestions for Improvement:**
- Use action verbs (e.g., “Led”, “Created”, “Analyzed”)
- Add measurable outcomes where possible (“Increased efficiency by 20%”)
- Keep it to one page unless you have >5 years of experience

🚀 You're on the right track! Tweak it and start applying!
    """
