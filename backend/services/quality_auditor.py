from services.gemini_service import ask_gemini

def audit_prompt_quality(prompt_text: str, rag_examples: list[str] = None) -> str:
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
    
    Uses pure, semantic, unanchored Gemini-based analysis to evaluate, score, and optimize the prompt.
    The evaluation is fully continuous, responsive, and realistic across the entire 0-100 scale.
    """
    
    rag_context = ""
    if rag_examples and len(rag_examples) > 0:
        rag_context = "\n[RAG SYSTEM LEARNING - PAST HIGH-QUALITY EXAMPLES]\n"
        rag_context += "The following are historical examples of highly optimized prompts from our database. Use these to infer the preferred style and structure when generating the optimized_prompt for this new input:\n"
        for idx, ex in enumerate(rag_examples):
            rag_context += f"--- EXAMPLE {idx+1} ---\n{ex}\n\n"

    query = f"""
You are a world-class Prompt Engineer and Principal AI Instructions Designer.
Perform a deep, realistic semantic evaluation of the following prompt against the 8 core pillars of Prompt Engineering Quality:

1. **Well-structured**: Usage of markdown headers, clear logical sections, structural delimiters (e.g. triple backticks, xml tags), and readability.
2. **Safe**: Resistance to prompt injection, jailbreak attempts, system instruction leakage, and data leakage/scraping.
3. **Optimized**: Clutter-free instructions, token efficiency, direct active voice, avoiding redundant fluff or self-contradictions.
4. **Context-rich**: Providing clear background, persona context, scenario setting, and defining explicit input/output variable fields.
5. **Role-specific**: Establishment of a precise expert persona with detailed style, voice, domain knowledge, and perspective guidelines.
6. **Hallucination-resistant**: Concrete negative constraints (what NOT to do), truthfulness guidelines, and clear instructions for handling out-of-scope/unknown questions.
7. **Reusable**: Use of templates, configurable variables (like [VARIABLE] or {{{{variable}}}}), and modular instruction blocks for repeatable executions.
8. **Professional**: Rigor of logical rules, enterprise-grade terminology, structured formatting, and professional tone.
{rag_context}

Prompt to evaluate:
---
{prompt_text}
---

CRITICAL REQUIREMENTS FOR HIGHLY RELATED & CUSTOM FEEDBACK:
- Never return generic, placeholder, or template text. Every single feedback, score, diagnostic check, and security issue MUST analyze the actual subject matter of the input prompt.
- Do NOT return generic prompt engineering advice (e.g., do NOT just say "add delimiters" or "be clear").
- Perform a thorough semantic evaluation. Evaluate the qualitative and functional strength of the instructions.

CRITICAL INSTRUCTIONS FOR REALISTIC & CONTINUOUS SCORING:
- Calculate a completely dynamic, continuous overall_score between 0 and 100 based on your expert qualitative assessment.
- Do NOT anchor to any default, sample, or boundary numbers. There are no fixed minimums or maximums.
- An extremely basic, empty, single-line, or brief prompt must receive a very low, realistic score (e.g., in the range of 10 to 35). An average prompt should be scored in the 50 to 75 range, and a highly engineered, production-ready prompt should receive a score above 90.
- The 8 individual metric scores (integers from 1 to 10) must represent the actual quality of each dimension and mathematically align with the final overall_score (e.g., if metric scores average around 3/10, the overall_score should be around 30/100).

- The "optimized_prompt" must be a fully developed, elite-engineered prompt coaching version designed specifically for this exact topic (do not use generic templates). It must include:
  1. An elite Expert Persona tailored to this task.
  2. Clear, high-performance Objectives.
  3. Concrete semantic Constraints and Negative Guardrails.
  4. Delimited Inputs and Configurable Placeholders (e.g. `[TEXT]` or `{{{{variable}}}}`).
  5. An explicit Output Format instruction.

Return a STRICT, valid JSON object. Do not wrap it in anything else, just the JSON. The JSON schema must contain the exact keys shown below.
DO NOT return the literal angle brackets or placeholder tags listed below; replace them with your actual calculated real evaluation values:

{{
  "overall_score": <calculated_score_between_0_and_100_integer>,
  "prompt_type": "<prompt_type_string_like_Prompt_Template_or_System_Prompt>",
  "metrics": {{
    "well_structured": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_structure_for_this_prompt>" }},
    "safe": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_safety_for_this_prompt>" }},
    "optimized": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_token_efficiency_for_this_prompt>" }},
    "context_rich": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_contextual_background_for_this_prompt>" }},
    "role_specific": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_persona_quality_for_this_prompt>" }},
    "hallucination_resistant": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_hallucination_resistance_for_this_prompt>" }},
    "reusable": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_reusability_for_this_prompt>" }},
    "professional": {{ "score": <calculated_metric_score_1_to_10_integer>, "status": "<pass_or_warning_or_fail>", "feedback": "<detailed_semantic_feedback_on_professionalism_and_logic_for_this_prompt>" }}
  }},
  "security_assessment": {{
    "risk_level": "<low_or_medium_or_high>",
    "issues": [<specific_identified_safety_or_security_vulnerabilities_as_strings>]
  }},
  "diagnostics": [
    {{
      "metric": "<metric_name>",
      "passed": <true_or_false>,
      "name": "<diagnostic_check_name>",
      "details": "<domain_specific_evaluation_details>"
    }}
  ],
  "optimized_prompt": "<Redesigned_elite_expert_prompt_coaching_version>"
}}
"""
    return ask_gemini(query, response_json=True)
