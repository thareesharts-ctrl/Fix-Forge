from services.gemini_service import ask_gemini

def analyze_prompt(prompt):

    query = f"""
You are an expert Prompt Engineer.

Analyze the following prompt:

---
{prompt}
---

Return STRICT JSON with:

{{
  "role": "",
  "task": "",
  "context": "",
  "constraints": "",
  "output_format": "",
  "issues": []
}}
"""

    return ask_gemini(query, response_json=True)
