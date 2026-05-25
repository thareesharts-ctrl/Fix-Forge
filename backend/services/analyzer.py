from services.qwen_service import ask_qwen

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

    return ask_qwen(query)