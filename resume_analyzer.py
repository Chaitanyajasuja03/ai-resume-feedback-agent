import openai
import streamlit as st

openai.api_key = st.secrets["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"]

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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']
