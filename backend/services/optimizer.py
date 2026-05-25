from services.qwen_service import ask_qwen

def optimize_prompt(prompt):

    query = f"""
Improve this prompt to professional level.

Add:
- clear role
- constraints
- examples if needed
- output format

Prompt:
{prompt}
"""

    return ask_qwen(query)