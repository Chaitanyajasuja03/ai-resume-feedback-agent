import requests
import streamlit as st

# Replace with any HF LLM that accepts plain text
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
}

def analyze_resume(resume_text):
    prompt = f"Give detailed, professional feedback on the following resume:\n\n{resume_text}"
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True  # This waits if the model is cold-starting
        }
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    try:
        output = response.json()
    except requests.exceptions.JSONDecodeError:
        return f"Error analyzing resume:\n\n{response.status_code} - Invalid JSON response"

    if response.status_code != 200:
        return f"Error analyzing resume:\n\n{response.status_code} - {output}"

    return output[0]['generated_text']
