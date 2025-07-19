import openai
import streamlit as st

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or gpt-4 if available
        messages=[
            {"role": "system", "content": "You are an expert resume analyzer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
