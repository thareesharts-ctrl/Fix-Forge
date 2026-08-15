<div align="center">

# ⚡ FixForge

### AI-Powered Prompt Engineering Quality Analyzer

*Stop guessing if your AI prompts are good. Know it for a fact.*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-AI_Engine-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![MongoDB](https://img.shields.io/badge/MongoDB_Atlas-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![n8n](https://img.shields.io/badge/n8n-Automation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

</div>

---

## 🧠 What is FixForge?

**FixForge** is a full-stack, AI-powered platform that analyzes, scores, and **automatically optimizes** your AI prompts against **8 core pillars of Prompt Engineering quality**. Powered by **Google Gemini**, FixForge acts as a world-class Prompt Engineer in your browser — giving you a deep diagnostic breakdown and a production-ready rewrite of every prompt you submit.

Whether you're building autonomous agents, chatbots, or LLM pipelines, FixForge ensures your instructions are **structurally sound, safe, and hallucination-resistant** before they ever hit production.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🏆 **8-Pillar Quality Audit** | Deep semantic evaluation across Structure, Safety, Optimization, Context, Role, Hallucination-Resistance, Reusability & Professionalism |
| 🤖 **AI-Powered Optimization** | Gemini auto-generates an elite, rewritten version of your prompt with expert personas, negative guardrails & configurable placeholders |
| 📊 **Live Score Dashboard** | Animated circular score gauge + per-pillar progress bars in a sleek dark/light-mode UI |
| 🗂️ **Batch File Analysis** | Drag-and-drop up to 5 `.md` / `.txt` / `.prompt` files and analyze them all simultaneously |
| 🔒 **Security Risk Assessment** | Detects prompt injection vulnerabilities, jailbreak surface area, and data leakage vectors |
| 🧬 **RAG-Enhanced Scoring** | Uses Gemini Embeddings + cosine similarity to learn from your best past prompts and improve future suggestions |
| 📜 **PDF Report Export** | One-click PDF download with a full structured report via the `/api/generate-pdf` endpoint |
| 📬 **n8n Email Automation** | Fully automated pipeline: email a `.md` file → receive a rich HTML analysis + PDF attachment back |
| 🕓 **Prompt History Library** | MongoDB-backed audit history with per-entry score badges and re-load capability |
| ⚡ **Multi-Key Load Balancing** | Supports multiple Gemini API keys with automatic shuffled failover for high-throughput usage |

---

## 🖥️ Screenshots

> *A real-time look at FixForge in action*

**Prompt Workspace & Score Hub**
```
┌───────────────────────────────────────┬──────────────────────────────────────┐
│  📝 Workspace                          │  📋 Diagnostics Hub                   │
│                                       │                                      │
│  [Drag & Drop or type your prompt]    │       ╭──────────╮                   │
│                                       │       │  87/100  │  ← Live Score     │
│  ┌─────────────────────────────────┐  │       ╰──────────╯                   │
│  │ RAW PROMPT INPUT                │  │   Status: OPTIMIZED ✅               │
│  │ Enter system instructions...    │  │                                      │
│  └─────────────────────────────────┘  │   Quality Dimensions (8 Pillars)     │
│                                       │   ████████░░ Well-Structured  8/10   │
│  [ 🔍 Evaluate Prompt Quality ]       │   ██████░░░░ Safe              6/10   │
│                                       │   █████████░ Optimized        9/10   │
│  ✨ Suggested Optimization:            │   ████████░░ Context-Rich     8/10   │
│  ┌─────────────────────────────────┐  │   ...                                │
│  │ [Elite rewritten prompt...]     │  │                                      │
│  │                                 │  │                                      │
│  │  [✓ Accept Changes & Re-Eval]   │  │                                      │
│  └─────────────────────────────────┘  │                                      │
└───────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         FixForge Platform                        │
│                                                                  │
│  ┌──────────────────┐     HTTP/REST     ┌────────────────────┐  │
│  │                  │ ──────────────▶  │                    │  │
│  │  React Frontend  │                  │  FastAPI Backend   │  │
│  │  (Vite + JSX)    │ ◀──────────────  │   (Python 3.11+)   │  │
│  │                  │    JSON Reports   │                    │  │
│  └──────────────────┘                  └────────┬───────────┘  │
│                                                 │              │
│                          ┌──────────────────────┼──────────┐   │
│                          │                      │          │   │
│                          ▼                      ▼          ▼   │
│                   ┌────────────┐    ┌──────────────┐  ┌──────┐ │
│                   │  Google    │    │  MongoDB     │  │ n8n  │ │
│                   │  Gemini AI │    │  Atlas (DB)  │  │      │ │
│                   │  (Engine)  │    │  RAG + Cache │  │ Auto │ │
│                   └────────────┘    └──────────────┘  └──────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔬 The 8 Pillars of Prompt Quality

FixForge evaluates every prompt against a rigorous 8-point rubric, scoring each from **1–10**:

```
🏛️  Well-Structured       — Markdown headers, logical sections, delimiters
🛡️  Safe                  — Injection resistance, jailbreak prevention, data leakage
⚡  Optimized             — Token efficiency, active voice, no contradictions
🗺️  Context-Rich          — Background context, scenario setting, I/O fields
👤  Role-Specific         — Expert persona, domain knowledge, style guidelines
🧠  Hallucination-Resist.  — Negative constraints, truthfulness rules, OOS handling
♻️  Reusable              — Template variables [LIKE_THIS], modular instruction blocks
💼  Professional          — Enterprise terminology, rigorous logic, structured format
```

The **Overall Score (0–100)** is calculated semantically by Gemini — not a simple average — providing a realistic, continuous assessment of prompt quality.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.11+**
- Node.js **18+**
- A **Google Gemini API Key** (free tier works) → [Get one here](https://aistudio.google.com/app/apikey)
- A **MongoDB Atlas** cluster (free M0 tier works) → [Sign up here](https://www.mongodb.com/cloud/atlas/register)

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/FixForge.git
cd FixForge
```

---

### 2️⃣ Configure the Backend

```bash
cd backend
```

Create a `.env` file:

```env
# .env — Backend Configuration
GEMINI_API_KEY=your_gemini_api_key_here
# Supports multiple keys for load balancing (comma-separated):
# GEMINI_API_KEY=key1,key2,key3

GEMINI_MODEL=gemini-1.5-flash

MONGODB_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/fixforge?retryWrites=true&w=majority
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app:app --reload --port 8000
```

✅ Backend is now running at `http://localhost:8000`
✅ API docs available at `http://localhost:8000/docs`

---

### 3️⃣ Launch the Frontend

```bash
cd ../frontend
npm install
npm run dev
```

✅ Frontend is now running at `http://localhost:5173`

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze` | Analyze a prompt from JSON body `{ "prompt": "..." }` |
| `POST` | `/api/analyze/file` | Analyze a `.md`, `.txt`, or `.prompt` file upload |
| `POST` | `/api/generate-pdf` | Generate a PDF report from analysis JSON |
| `GET` | `/api/history` | Retrieve the last 15 evaluated prompts |
| `GET` | `/api/health` | Health check for backend + database status |

### Example Request

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt": "You are a helpful assistant. Answer user questions."}'
```

### Example Response

```json
{
  "overall_score": 23,
  "prompt_type": "System Prompt",
  "metrics": {
    "well_structured": { "score": 2, "status": "fail", "feedback": "No markdown sections, headers, or structural delimiters present." },
    "safe": { "score": 3, "status": "fail", "feedback": "No injection resistance or jailbreak guardrails defined." },
    "hallucination_resistant": { "score": 1, "status": "fail", "feedback": "No constraints on what NOT to answer or how to handle unknown topics." }
  },
  "security": { "risk_level": "high", "issues": ["No system boundary defined", "Susceptible to role-play injection"] },
  "optimization": {
    "improved_prompt": "## SYSTEM IDENTITY\nYou are [EXPERT_ROLE], a specialized AI assistant..."
  }
}
```

---

## 🤖 n8n Email Automation

FixForge includes a fully automated email pipeline powered by **n8n**:

```
📧 You send email       →    📎 Attach .md or .txt prompt file
     ↓
🔍 n8n watches inbox   →    📤 Sends file to /api/analyze/file
     ↓
🧠 Gemini analyzes     →    📄 Generates PDF via /api/generate-pdf
     ↓
✉️  n8n replies back   →    📊 Rich HTML score table + report.pdf attachment
```

**Setup:** Import `n8n_workflow_v2.json` into your n8n instance and follow the [Complete n8n Setup Guide](FixForge-Complete-n8n-Setup-Guide.md).

---

## 📁 Project Structure

```
FixForge/
│
├── 📂 backend/
│   ├── app.py                    # FastAPI app entry point
│   ├── .env                      # Environment variables (not committed)
│   ├── requirements.txt          # Python dependencies
│   ├── 📂 routes/
│   │   └── analyze.py            # All API endpoints + PDF generation + RAG logic
│   ├── 📂 services/
│   │   ├── gemini_service.py     # Gemini API client (text + embeddings, multi-key)
│   │   ├── quality_auditor.py    # 8-pillar prompt evaluation engine
│   │   ├── analyzer.py           # Core analyzer orchestration
│   │   ├── optimizer.py          # Prompt optimization service
│   │   ├── scorer.py             # Scoring logic
│   │   └── security.py           # Security analysis helpers
│   └── 📂 config/
│       └── database.py           # MongoDB Atlas async client
│
├── 📂 frontend/
│   ├── index.html                # App entry HTML
│   ├── 📂 src/
│   │   ├── App.jsx               # Main React app (tabbed workspace + results)
│   │   ├── App.css               # Full design system & animations
│   │   └── main.jsx              # React app bootstrapper
│   └── package.json              # Node dependencies (Vite, React 19)
│
├── n8n_workflow.json             # n8n automation workflow (v1)
├── n8n_workflow_v2.json          # n8n automation workflow (v2 — PDF support)
├── FixForge-Complete-n8n-Setup-Guide.md
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19, Vite 8, Vanilla CSS |
| **Backend** | Python, FastAPI, Uvicorn |
| **AI Engine** | Google Gemini 1.5 Flash (via REST API) |
| **Embeddings** | Gemini Embedding v2 (for RAG) |
| **Database** | MongoDB Atlas (Motor async driver) |
| **PDF Generation** | ReportLab |
| **Automation** | n8n (self-hosted) |

---

## 🔧 Advanced Configuration

### Multi-Key Load Balancing

Add multiple Gemini API keys to avoid rate limits on free-tier accounts:

```env
GEMINI_API_KEY=key_A,key_B,key_C
```

FixForge will randomly shuffle and failover across all keys per request.

### RAG System

The backend automatically:
1. Embeds every analyzed prompt using Gemini Embedding v2
2. Stores high-scoring prompts (score ≥ 50) in MongoDB
3. On new analyses, retrieves the **2 most similar** past top-quality prompts via cosine similarity
4. Injects them as few-shot examples into the Gemini evaluation prompt to improve optimization quality over time

### Deterministic Caching

Identical prompts are SHA-256 hashed and cached in MongoDB — subsequent analyses of the same prompt return instantly without consuming API quota.

---

## 🗺️ Roadmap

- [ ] 🔐 User authentication & multi-user workspaces
- [ ] 📈 Analytics dashboard with score trends over time  
- [ ] 🔗 VS Code extension for in-editor prompt auditing
- [ ] 🌐 Public prompt benchmark leaderboard
- [ ] 🤝 Team collaboration with shared prompt libraries
- [ ] 🔄 Support for additional AI providers (OpenAI, Claude, Mistral)
- [ ] 📱 Mobile-responsive UI improvements

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ and 🔥 by the FixForge team**

*If FixForge helped you build better AI prompts, please give it a ⭐*

</div>
