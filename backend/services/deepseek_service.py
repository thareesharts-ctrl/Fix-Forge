import os
import requests
from dotenv import load_dotenv

# Load .env file with absolute path relative to this service file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
URL = "https://api.deepseek.com/chat/completions"


def ask_deepseek(prompt: str):
    """
    Executes a prompt completion call against the official DeepSeek API.
    """
    if not API_KEY:
        raise Exception("DEEPSEEK_API_KEY is not configured in your .env environment file.")
        
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
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
        "max_tokens": 2000
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        res_data = response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Official DeepSeek API request failed: {str(e)}")

    if "error" in res_data:
        err_msg = res_data["error"].get("message", "Unknown DeepSeek API error")
        raise Exception(f"DeepSeek API returned an error: {err_msg}")
        
    try:
        return res_data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise Exception(f"Failed to parse DeepSeek response format: {str(e)}")
