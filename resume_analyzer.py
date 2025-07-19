import requests
import streamlit as st
import json

# Hugging Face Inference API (must be a text-generation model)
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}",
    "Content-Type": "application/json"
}

def analyze_resume(resume_text):
    prompt = f"Give detailed, professional feedback on the following resume:\n\n{resume_text}"
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    try:
        output = response.json()
    except requests.exceptions.JSONDecodeError:
        return f"❌ Error analyzing resume:\n\n{response.status_code} - Invalid JSON returned by Hugging Face API.\nRaw response:\n{response.text}"

    if response.status_code != 200:
        return f"❌ Error analyzing resume:\n\n{response.status_code} - {output}"

    # Check the expected output structure
    if isinstance(output, list) and 'generated_text' in output[0]:
        return output[0]['generated_text']
    elif isinstance(output, dict) and 'error' in output:
        return f"❌ API Error: {output['error']}"
    else:
        return f"⚠️ Unexpected response structure:\n\n{output}"
