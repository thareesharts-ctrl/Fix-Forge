import os
import requests
import random
from dotenv import load_dotenv

# Load .env file with absolute path relative to this service file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

API_KEYS_RAW = os.getenv("GEMINI_API_KEY", "")
API_KEYS = [k.strip() for k in API_KEYS_RAW.split(",") if k.strip()]
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


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
            "topK": 1,
            "topP": 0.1
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
            
            # If rate-limited, quota exceeded, or server error, fallback to the next key
            if response.status_code in [429, 403] or response.status_code >= 500:
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

def get_gemini_embedding(text: str) -> list[float]:
    """
    Calls the Gemini Embedding API to generate a vector representation of the text.
    Supports load balancing across multiple API keys.
    """
    if not API_KEYS or API_KEYS[0] == "your_gemini_api_key_here":
        raise Exception("GEMINI_API_KEY is not configured.")

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "models/gemini-embedding-2",
        "content": {
            "parts": [{"text": text}]
        }
    }

    # Create a shuffled list of keys to load-balance
    keys_to_try = list(API_KEYS)
    random.shuffle(keys_to_try)
    
    last_error = None

    for key in keys_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent?key={key}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            # If rate-limited, quota exceeded, or server error, fallback to next key
            if response.status_code in [429, 403] or response.status_code >= 500:
                last_error = f"HTTP {response.status_code}: {response.text}"
                continue
                
            response.raise_for_status()
            res_data = response.json()
            
            if "embedding" in res_data and "values" in res_data["embedding"]:
                return res_data["embedding"]["values"]
            else:
                raise Exception(f"Failed to get embedding from Gemini: {res_data}")
                
        except requests.exceptions.RequestException as e:
            last_error = f"RequestException: {str(e)}"
            continue

    raise Exception(f"Google Gemini Embedding API failed for all keys. Last error: {last_error}")
