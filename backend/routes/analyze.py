from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import Response
from pydantic import BaseModel
from config.database import db
import json
import re
import numpy as np
from datetime import datetime
import io
import hashlib
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Import unified auditor service and embeddings
from services.quality_auditor import audit_prompt_quality
from services.gemini_service import get_gemini_embedding

router = APIRouter(prefix="/api", tags=["analyze"])

class PromptRequest(BaseModel):
    prompt: str

def clean_json_response(raw_string: str) -> dict:
    """Helper to extract and load JSON from LLM response safely, stripping code fences and sanitizing syntax errors."""
    if not raw_string:
        return {}
    
    raw_string = raw_string.strip()
    
    # Try direct parse first before any modifications (very safe for strict JSON providers like Gemini)
    try:
        return json.loads(raw_string)
    except Exception:
        pass

    # Strip markdown code fences if present
    if raw_string.startswith("```"):
        raw_string = re.sub(r"^```[a-zA-Z0-9]*\s*", "", raw_string)
        raw_string = re.sub(r"\s*```$", "", raw_string)
        
    # Try parsing again after stripping fences
    try:
        return json.loads(raw_string)
    except Exception:
        pass

    # Try finding the first '{' and last '}' to strip any conversational prefix/suffix
    start = raw_string.find('{')
    end = raw_string.rfind('}')
    
    if start == -1 or end == -1:
        return {"raw": raw_string}
        
    cleaned = raw_string[start:end+1].strip()
    
    # Try standard parse on extracted braces
    try:
        return json.loads(cleaned)
    except Exception:
        pass
    
    # Quote unquoted keys (like metric: -> "metric":) only if it fails to parse directly
    try:
        quoted = re.sub(r'([{,\s]+)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', cleaned)
        return json.loads(quoted)
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
    """Helper to coordinate prompt engineering audits using the unified Quality Auditor with RAG."""
    if not prompt_text.strip():
        raise HTTPException(status_code=400, detail="Prompt text cannot be empty")
        
    try:
        # 0. Deterministic Caching: Check if this exact prompt was already evaluated
        prompt_hash = hashlib.sha256(prompt_text.strip().encode("utf-8")).hexdigest()
        existing_report = await db.prompts.find_one({"prompt_hash": prompt_hash})
        if existing_report:
            existing_report.pop("_id", None)
            existing_report.pop("embedding", None)
            return existing_report

        # 1. RAG Retrieval Phase: Get embedding for new prompt
        input_embedding = None
        rag_examples = []
        try:
            input_embedding = get_gemini_embedding(prompt_text)
            
            # Fetch past high-scoring prompts that have embeddings
            cursor = db.prompts.find({"embedding": {"$exists": True}, "overall_score": {"$gte": 80}}).limit(100)
            past_prompts = []
            async for doc in cursor:
                past_prompts.append(doc)
            
            # Compute Cosine Similarity
            if input_embedding and past_prompts:
                v1 = np.array(input_embedding)
                scored_prompts = []
                for p in past_prompts:
                    v2 = np.array(p["embedding"])
                    sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                    scored_prompts.append((sim, p.get("optimization", {}).get("improved_prompt", p["prompt"])))
                
                # Sort by similarity and get top 2
                scored_prompts.sort(key=lambda x: x[0], reverse=True)
                rag_examples = [x[1] for x in scored_prompts[:2]]
        except Exception as e:
            print(f"RAG retrieval skipped or failed: {e}")

        # 2. Call unified Quality Auditor with RAG examples
        raw_audit = audit_prompt_quality(prompt_text, rag_examples=rag_examples)
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

        # Embed and Save to MongoDB if score is decent (to fuel future RAG)
        try:
            evaluation_report["prompt_hash"] = prompt_hash
            if overall_score >= 50 and input_embedding:
                evaluation_report["embedding"] = input_embedding
            
            # We set a maxTimeMS or timeout to prevent blocking if MongoDB is down
            await db.prompts.insert_one(evaluation_report.copy())
        except Exception as db_err:
            print(f"Database offline, skipped history logging: {db_err}")

        # MongoDB _id is not JSON serializable directly, pop it before returning
        evaluation_report.pop("_id", None)
        # Pop embedding so we don't send huge arrays to the frontend
        evaluation_report.pop("embedding", None)
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

@router.post("/generate-pdf")
async def generate_pdf_report(data: dict = Body(...)):
    """Generate a PDF report from analysis JSON data."""
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        elements.append(Paragraph("Prompt Analysis Report", styles['Title']))
        elements.append(Spacer(1, 20))
        
        # Summary Section
        elements.append(Paragraph(f"<b>Overall Score:</b> {data.get('overall_score', 'N/A')} / 100", styles['Normal']))
        elements.append(Paragraph(f"<b>Prompt Type:</b> {data.get('prompt_type', 'N/A')}", styles['Normal']))
        
        security = data.get('security', {})
        risk_level = security.get('risk_level', 'N/A').upper()
        elements.append(Paragraph(f"<b>Security Risk:</b> {risk_level}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Original Prompt
        elements.append(Paragraph("<b>Original Prompt:</b>", styles['Heading2']))
        original_prompt = data.get('prompt', 'N/A')
        elements.append(Preformatted(original_prompt, styles['Code']))
        elements.append(Spacer(1, 20))
        
        # Optimized Prompt
        elements.append(Paragraph("<b>Optimized Prompt:</b>", styles['Heading2']))
        optimized_prompt = data.get('optimization', {}).get('improved_prompt', 'N/A')
        elements.append(Preformatted(optimized_prompt, styles['Code']))
        
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

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