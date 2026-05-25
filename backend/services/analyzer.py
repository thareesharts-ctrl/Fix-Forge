from services.deepseek_service import ask_deepseek

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

    return ask_deepseek(query)