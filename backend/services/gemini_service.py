import os
import requests
import random
from dotenv import load_dotenv

# Load .env file with absolute path relative to this service file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

API_KEYS_RAW = os.getenv("GEMINI_API_KEY", "")
API_KEYS = [k.strip() for k in API_KEYS_RAW.split(",") if k.strip()]
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def ask_gemini(prompt: str, response_json: bool = False):
    """
    Executes a prompt completion call against the official Google Gemini API via HTTP POST.
    Supports load balancing across multiple API keys.
    """
    if not API_KEYS or API_KEYS[0] == "your_gemini_api_key_here":
        raise Exception("GEMINI_API_KEY is not configured in your .env environment file.")

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
            "temperature": 0.0,
        }
    }

    if response_json:
        payload["generationConfig"]["responseMimeType"] = "application/json"

    # Create a shuffled list of keys to load-balance
    keys_to_try = list(API_KEYS)
    random.shuffle(keys_to_try)
    
    last_error = None

    for key in keys_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            # If rate-limited or server error, fallback to the next key
            if response.status_code == 429 or response.status_code >= 500:
                last_error = f"HTTP {response.status_code}: {response.text}"
                continue
                
            response.raise_for_status()
            res_data = response.json()
            
            if "candidates" not in res_data or not res_data["candidates"]:
                if "error" in res_data:
                    err_msg = res_data["error"].get("message", "Unknown error response")
                    raise Exception(f"Gemini API Error: {err_msg}")
                raise Exception(f"Gemini API returned an empty or invalid candidate structure: {res_data}")

            try:
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                raise Exception(f"Failed to parse Gemini response text: {str(e)}")
                
        except requests.exceptions.RequestException as e:
            last_error = f"RequestException: {str(e)}"
            continue

    # If the loop finishes without returning, all keys failed
    raise Exception(f"Google Gemini API request failed for all available keys. Last error: {last_error}")
