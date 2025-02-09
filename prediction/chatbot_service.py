import requests
from django.conf import settings

gemini_api_key = "your-api-key"

disaster_prompts = {
    "before": "Provide disaster preparedness tips and warnings before an event.",
    "during": "Provide emergency response steps during a disaster event.",
    "after": "Provide recovery and relief information after a disaster event."
}

def get_chat_response(phase, prompt):
    phase_prompt = disaster_prompts.get(phase, "")
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-model",
        "messages": [
            {"role": "system", "content": phase_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://api.gemini.com/v1/chat/completions", headers=headers, json=data)
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]