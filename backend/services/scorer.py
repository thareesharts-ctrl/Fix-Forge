from services.deepseek_service import ask_deepseek

def score_prompt(prompt):

    query = f"""
Score this prompt (0-100) based on:

- clarity
- structure
- completeness
- safety
- output control

Return JSON only:
{{
  "score": number,
  "reason": "short explanation"
}}

Prompt:
{prompt}
"""

    return ask_deepseek(query)