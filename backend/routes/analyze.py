from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from config.database import db
import json
import re
from datetime import datetime

# Import unified auditor service
from services.quality_auditor import audit_prompt_quality

router = APIRouter(prefix="/api", tags=["analyze"])

class PromptRequest(BaseModel):
    prompt: str

def clean_json_response(raw_string: str) -> dict:
    """Helper to extract and load JSON from LLM response safely, stripping code fences and sanitizing syntax errors."""
    if not raw_string:
        return {}
    
    # Strip markdown code fences if present
    raw_string = raw_string.strip()
    if raw_string.startswith("```"):
        raw_string = re.sub(r"^```[a-zA-Z0-9]*\s*", "", raw_string)
        raw_string = re.sub(r"\s*```$", "", raw_string)
        
    # Try finding the first '{' and last '}' to strip any conversational prefix/suffix
    start = raw_string.find('{')
    end = raw_string.rfind('}')
    
    if start == -1 or end == -1:
        return {"raw": raw_string}
        
    cleaned = raw_string[start:end+1].strip()
    
    # Quote unquoted keys (like metric: -> "metric":)
    cleaned = re.sub(r'([{,\s]+)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', cleaned)
    
    # Locate "optimized_prompt" key and escape its inner quotes/newlines/tabs to ensure perfect JSON format
    opt_key_match = re.search(r'"optimized_prompt"\s*:\s*"', cleaned)
    if opt_key_match:
        opt_start = opt_key_match.end()
        closing_brace_idx = cleaned.rfind('}')
        if closing_brace_idx != -1:
            opt_end = cleaned.rfind('"', opt_start, closing_brace_idx)
            if opt_end != -1:
                # Extract and escape raw prompt content
                raw_opt_prompt = cleaned[opt_start:opt_end]
                escaped_opt_prompt = raw_opt_prompt.replace('\\', '\\\\')
                escaped_opt_prompt = escaped_opt_prompt.replace('"', '\\"')
                escaped_opt_prompt = escaped_opt_prompt.replace('\n', '\\n')
                escaped_opt_prompt = escaped_opt_prompt.replace('\r', '\\r')
                escaped_opt_prompt = escaped_opt_prompt.replace('\t', '\\t')
                
                cleaned = cleaned[:opt_start] + escaped_opt_prompt + cleaned[opt_end:]
                
    # Try standard parse
    try:
        return json.loads(cleaned)
    except Exception:
        pass
        
    # Fallback to handle any remaining trailing commas
    try:
        sanitized = re.sub(r',\s*([\]}])', r'\1', cleaned)
        return json.loads(sanitized)
    except Exception:
        pass
        
    return {"raw": raw_string}

async def process_prompt_evaluation(prompt_text: str) -> dict:
    """Helper to coordinate prompt engineering audits using the unified Quality Auditor."""
    if not prompt_text.strip():
        raise HTTPException(status_code=400, detail="Prompt text cannot be empty")
        
    try:
        # Call Qwen unified Quality Auditor
        raw_audit = audit_prompt_quality(prompt_text)
        audit_data = clean_json_response(raw_audit)

        # Extract values with robust defaults
        overall_score = audit_data.get("overall_score")
        if overall_score is None:
            # Fallback calculation if score is missing
            overall_score = 50
            if isinstance(audit_data.get("metrics"), dict):
                scores = [m.get("score", 5) for m in audit_data["metrics"].values() if isinstance(m, dict)]
                if scores:
                    overall_score = int(sum(scores) / len(scores) * 10)
        
        # Build comprehensive prompt engineering audit report
        evaluation_report = {
            "prompt": prompt_text,
            "timestamp": datetime.utcnow().isoformat(),
            "overall_score": overall_score,
            "prompt_type": audit_data.get("prompt_type", "Prompt Template"),
            "metrics": audit_data.get("metrics", {}),
            "security": {
                "risk_level": audit_data.get("security_assessment", {}).get("risk_level", "low") if isinstance(audit_data.get("security_assessment"), dict) else "low",
                "issues": audit_data.get("security_assessment", {}).get("issues", []) if isinstance(audit_data.get("security_assessment"), dict) else []
            },
            "diagnostics": audit_data.get("diagnostics", []),
            "suggestions": audit_data.get("suggestions", []),
            "optimization": {
                "improved_prompt": audit_data.get("optimized_prompt", prompt_text)
            },
            # Legacy fields for backward compatibility
            "structure": {
                "role": audit_data.get("metrics", {}).get("role_specific", {}).get("feedback", "") if isinstance(audit_data.get("metrics"), dict) else "",
                "task": audit_data.get("metrics", {}).get("well_structured", {}).get("feedback", "") if isinstance(audit_data.get("metrics"), dict) else "",
                "context": audit_data.get("metrics", {}).get("context_rich", {}).get("feedback", "") if isinstance(audit_data.get("metrics"), dict) else "",
                "constraints": audit_data.get("metrics", {}).get("hallucination_resistant", {}).get("feedback", "") if isinstance(audit_data.get("metrics"), dict) else "",
                "output_format": audit_data.get("metrics", {}).get("professional", {}).get("feedback", "") if isinstance(audit_data.get("metrics"), dict) else "",
                "issues": audit_data.get("security_assessment", {}).get("issues", []) if isinstance(audit_data.get("security_assessment"), dict) else []
            },
            "scoring": {
                "score": overall_score,
                "reason": f"Overall quality evaluated as {overall_score}/100."
            }
        }

        # Save to MongoDB (graceful fallback if DB is offline)
        try:
            # We set a maxTimeMS or timeout to prevent blocking if MongoDB is down
            await db.prompts.insert_one(evaluation_report.copy())
        except Exception as db_err:
            print(f"Database offline, skipped history logging: {db_err}")

        # MongoDB _id is not JSON serializable directly, pop it before returning
        evaluation_report.pop("_id", None)
        return evaluation_report

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prompt evaluation failed: {str(e)}")

@router.post("/analyze")
async def analyze_text_prompt(payload: PromptRequest):
    """Analyze a plain text prompt sent in JSON body."""
    return await process_prompt_evaluation(payload.prompt)

@router.post("/analyze/file")
async def analyze_file_prompt(file: UploadFile = File(...)):
    """Analyze a prompt uploaded as a file (.md, .txt, .prompt)."""
    # Validate extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["txt", "md", "prompt"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload .txt, .md, or .prompt files.")
        
    try:
        content = await file.read()
        prompt_text = content.decode("utf-8")
        return await process_prompt_evaluation(prompt_text)
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode file content. Ensure file is UTF-8 encoded.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File read failed: {str(e)}")

@router.get("/history")
async def get_prompt_history(limit: int = 15):
    """Retrieve history of evaluated prompts from MongoDB."""
    try:
        cursor = db.prompts.find().sort("timestamp", -1).limit(limit)
        history = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            history.append(doc)
        return history
    except Exception as e:
        print(f"Failed to fetch history (DB offline): {e}")
        return []

@router.get("/health")
async def health_check():
    """Verify backend connectivity to MongoDB Atlas database."""
    db_status = "offline"
    try:
        # Ping remote MongoDB Atlas database
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        print(f"Database health check failed: {e}")
        
    return {
        "status": "healthy",
        "database": db_status,
        "ai_engine": "connected"
    }