import os
import requests
from dotenv import load_dotenv

# Load .env file with absolute path relative to qwen_service.py
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)


API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_qwen(prompt: str):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "FixForge"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 1500
    }

    response = requests.post(URL, headers=headers, json=payload)
    res_data = response.json()
    
    if "error" in res_data:
        raise Exception(res_data["error"].get("message", "Unknown OpenRouter API error"))
        
    return res_data["choices"][0]["message"]["content"]