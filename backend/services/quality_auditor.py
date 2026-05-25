from services.gemini_service import ask_gemini

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
    
    Returns a strict JSON string matching the Prompt Quality schema.
    """
    
    query = f"""
You are a world-class Prompt Engineer and Principal AI Instructions Designer.
Evaluate the following prompt against the 8 core pillars of Prompt Engineering Quality:

1. **Well-structured**: Usage of markdown headers, clear logical sections, structural delimiters (e.g. triple backticks, xml tags), and readability.
2. **Safe**: Resistance to prompt injection, jailbreak attempts, system instruction leakage, and data leakage/scraping.
3. **Optimized**: Clutter-free instructions, token efficiency, direct active voice, avoiding redundant fluff or self-contradictions.
4. **Context-rich**: Providing clear background, persona context, scenario setting, and defining explicit input/output variable fields.
5. **Role-specific**: Establishment of a precise expert persona with detailed style, voice, domain knowledge, and perspective guidelines.
6. **Hallucination-resistant**: Concrete negative constraints (what NOT to do), truthfulness guidelines, and clear instructions for handling out-of-scope/unknown questions.
7. **Reusable**: Use of templates, configurable variables (like [VARIABLE] or {{{{variable}}}}), and modular instruction blocks for repeatable executions.
8. **Professional**: Rigor of logical rules, enterprise-grade terminology, structured formatting, and professional tone.

Prompt to evaluate:
---
{prompt_text}
---

CRITICAL REQUIREMENTS FOR HIGHLY RELATED & CUSTOM FEEDBACK:
- Never return generic, placeholder, or template text. Every single feedback, suggestion, and security issue MUST analyze the actual subject matter of the input prompt.
- Do NOT return generic prompt engineering advice (e.g., do NOT just say "add delimiters" or "be clear").
- The "suggestions" array must contain 3 to 5 highly specific, actionable coaching advices that target the precise logic, domain constraints, or system rules of the input prompt.
- The "optimized_prompt" must be a fully developed, elite-engineered prompt coaching version designed specifically for this exact topic (do not use generic templates). It must include:
  1. An elite Expert Persona tailored to this task.
  2. Clear, high-performance Objectives.
  3. Concrete semantic Constraints and Negative Guardrails.
  4. Delimited Inputs and Configurable Placeholders (e.g. `[TEXT]` or `{{{{variable}}}}`).
  5. An explicit Output Format instruction.

Return a STRICT, valid JSON object. Do not wrap it in anything else, just the JSON. The JSON schema must be exactly:
{{
  "overall_score": 82, // 0-100 overall score
  "prompt_type": "Prompt Template", // "Prompt", "Prompt Template", "AI Instruction", "Role Prompt", "Agent Prompt", or "System Prompt"
  "metrics": {{
    "well_structured": {{ "score": 8, "status": "pass", "feedback": "Detailed structural analysis of how this specific topic is structured..." }},
    "safe": {{ "score": 9, "status": "pass", "feedback": "Detailed security audit of specific vulnerabilities in this prompt's domain..." }},
    "optimized": {{ "score": 7, "status": "warning", "feedback": "Token and wording efficiency feedback for this specific instruction..." }},
    "context_rich": {{ "score": 6, "status": "warning", "feedback": "Domain background and detail advice for this specific topic..." }},
    "role_specific": {{ "score": 8, "status": "pass", "feedback": "Persona quality feedback specific to this expert domain..." }},
    "hallucination_resistant": {{ "score": 5, "status": "fail", "feedback": "Negative constraints advice for this specific logic..." }},
    "reusable": {{ "score": 4, "status": "fail", "feedback": "Variable and templating suggestions for this specific topic..." }},
    "professional": {{ "score": 7, "status": "pass", "feedback": "Rigorous domain logic feedback for this specific topic..." }}
  }},
  "security_assessment": {{
    "risk_level": "low", // "low", "medium", or "high"
    "issues": [] // Specific identified safety/security vulnerabilities in this prompt's domain
  }},
  "diagnostics": [
    {{
      "metric": "well_structured",
      "passed": true,
      "name": "Topic-Specific Structural Review",
      "details": "Contextual detail about how the prompt structured this specific topic."
    }}
  ],
  "suggestions": [
    // Provide 3-5 highly contextual suggestions directly addressing the logic, code, rules, or inputs of this prompt.
  ],
  "optimized_prompt": "Redesigned expert prompt coaching version..."
}}
"""
    return ask_gemini(query, response_json=True)


