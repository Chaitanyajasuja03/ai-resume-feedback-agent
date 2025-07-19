import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
HF_TOKEN = st.secrets["HF_API_TOKEN"]  # Store your Hugging Face token in .streamlit/secrets.toml

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

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

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 512},
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error analyzing resume:\n\n{response.status_code} - {response.json()}"
