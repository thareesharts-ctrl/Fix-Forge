from services.qwen_service import ask_qwen

def audit_prompt_quality(prompt_text: str) -> str:
    """
    Performs a unified, highly detailed evaluation of an AI prompt against the 8 core pillars of Prompt Engineering Quality:
    1. Well-structured
    2. Safe
    3. Optimized
    4. Context-rich
    5. Role-specific
    6. Hallucination-resistant
    7. Reusable
    8. Professional
    
    Returns a JSON string matching the Prompt Quality schema.
    """
    
    query = f"""
You are a world-class Prompt Engineer and Principal AI Instructions Designer.
Evaluate the following prompt against the 8 core pillars of Prompt Engineering Quality:

1. **Well-structured**: Usage of markdown headers, clear logical sections, structural delimiters (e.g. triple backticks, xml tags), and readability.
2. **Safe**: Resistance to prompt injection, jailbreak attempts, system instruction leakage, and data leakage/scraping.
3. **Optimized**: Clutter-free instructions, token efficiency, direct active voice, avoiding redundant fluff or self-contradictions.
4. **Context-rich**: Providing clear background, persona context, scenario setting, and defining explicit input/output variable fields.
5. **Role-specific**: Establishment of a precise expert persona with detailed style, voice, domain knowledge, and perspective guidelines.
6. **Hallucination-resistant**: Concrete negative constraints (what NOT to do), truthfulness guidelines, and clear instructions for handling out-of-scope/unknown questions (e.g., "If you do not know, say 'I don't know'").
7. **Reusable**: Use of templates, configurable variables (like [VARIABLE] or {{{{variable}}}}), and modular instruction blocks for repeatable executions.
8. **Professional**: Rigor of logical rules, enterprise-grade terminology, structured formatting, and professional tone.

Prompt to evaluate:
---
{prompt_text}
---

Return a STRICT, valid JSON object. Do not wrap it in anything else, just the JSON. The JSON schema must be exactly:
{{
  "overall_score": 82, // 0-100 overall score
  "prompt_type": "Prompt Template", // "Prompt", "Prompt Template", "AI Instruction", "Role Prompt", "Agent Prompt", or "System Prompt"
  "metrics": {{
    "well_structured": {{ "score": 8, "status": "pass", "feedback": "Feedback for structured..." }},
    "safe": {{ "score": 9, "status": "pass", "feedback": "Feedback for safe..." }},
    "optimized": {{ "score": 7, "status": "warning", "feedback": "Feedback for optimized..." }},
    "context_rich": {{ "score": 6, "status": "warning", "feedback": "Feedback for context..." }},
    "role_specific": {{ "score": 8, "status": "pass", "feedback": "Feedback for role..." }},
    "hallucination_resistant": {{ "score": 5, "status": "fail", "feedback": "Feedback for hallucination..." }},
    "reusable": {{ "score": 4, "status": "fail", "feedback": "Feedback for reusable..." }},
    "professional": {{ "score": 7, "status": "pass", "feedback": "Feedback for professional..." }}
  }},
  "security_assessment": {{
    "risk_level": "low", // "low", "medium", or "high"
    "issues": ["Issue 1"] // List of identified vulnerabilities
  }},
  "diagnostics": [
    {{
      "metric": "well_structured",
      "passed": true,
      "name": "Markdown Structure",
      "details": "The prompt successfully utilizes markdown titles for separation."
    }}
  ],
  "suggestions": [
    "Add explicit delimiters around input variables.",
    "Add a negative constraint to prevent model hallucinations."
  ],
  "optimized_prompt": "Redesigned version of prompt..." // The complete, redesigned, highly professional, perfectly formatted version of the prompt. If the input prompt is weak or wrong, you MUST restructure it into the absolute perfect prompt structure including: 1. ## Persona & Role, 2. ## Objective & Task, 3. ## Context & Background, 4. ## Constraints & Negative Guardrails (such as hallucination protection and jailbreak prevention), 5. ## Dynamic Variables (using [VARIABLES] or {{bracket}} variables), and 6. ## Expected Output Format. Ensure this is beautifully formatted with markdown headings and clear section dividers.
}}
"""
    return ask_qwen(query)
