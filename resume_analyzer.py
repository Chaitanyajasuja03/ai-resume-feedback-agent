import requests
import streamlit as st
import json

# Use Falcon-7B-Instruct, which works with free-tier tokens
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

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
    except json.decoder.JSONDecodeError:
        return f"❌ JSON Decode Error:\nStatus: {response.status_code}\nRaw response: {response.text}"

    if response.status_code != 200:
        return f"❌ API Error:\nStatus: {response.status_code}\nDetails: {output}"

    # Falcon returns generated_text inside list
    if isinstance(output, list) and 'generated_text' in output[0]:
        return output[0]['generated_text']

    return f"⚠️ Unexpected response:\n{output}"
