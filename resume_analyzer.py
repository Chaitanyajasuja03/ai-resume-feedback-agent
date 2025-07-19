import requests
import streamlit as st

# Replace with any HF LLM that accepts plain text
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
}

def analyze_resume(resume_text):
    prompt = f"""
You are an expert career coach. Analyze the following resume:

\"\"\"{resume_text}\"\"\"

Give feedback on:
1. Structure and formatting
2. Grammar and clarity
3. Missing important sections
4. Industry relevance
5. Specific improvement tips
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
