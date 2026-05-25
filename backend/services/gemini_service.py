import os
import requests
from dotenv import load_dotenv

# Load .env file with absolute path relative to this service file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def ask_gemini(prompt: str, response_json: bool = False):
    """
    Executes a prompt completion call against the official Google Gemini API via HTTP POST.
    """
    if not API_KEY or API_KEY == "your_gemini_api_key_here":
        raise Exception("GEMINI_API_KEY is not configured in your .env environment file.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
        }
    }

    if response_json:
        payload["generationConfig"]["responseMimeType"] = "application/json"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        res_data = response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Google Gemini API request failed: {str(e)}")

    if "candidates" not in res_data or not res_data["candidates"]:
        if "error" in res_data:
            err_msg = res_data["error"].get("message", "Unknown error response")
            raise Exception(f"Gemini API Error: {err_msg}")
        raise Exception(f"Gemini API returned an empty or invalid candidate structure: {res_data}")

    try:
        return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        raise Exception(f"Failed to parse Gemini response text: {str(e)}")
