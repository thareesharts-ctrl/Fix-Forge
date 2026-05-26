import { useState, useRef, useEffect } from 'react'
import './App.css'

const API_URL = "http://127.0.0.1:8000/api";

function App() {
  const [prompt, setPrompt] = useState("");
  const [backendAvailable, setBackendAvailable] = useState(false);
  const [dbConnected, setDbConnected] = useState(false);
  const [isAuditing, setIsAuditing] = useState(false);
  const [report, setReport] = useState(null);
  const [history, setHistory] = useState([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [fileName, setFileName] = useState("");
  const [loadingMessage, setLoadingMessage] = useState(null);
  const [theme, setTheme] = useState("dark");
  const [copied, setCopied] = useState(false);
  
  const fileInputRef = useRef(null);

  useEffect(() => {
    checkConnection();
  }, []);

  useEffect(() => {
    if (theme === "light") {
      document.body.classList.add("light-mode");
    } else {
      document.body.classList.remove("light-mode");
    }
  }, [theme]);

  const checkConnection = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      if (response.ok) {
        const data = await response.json();
        setBackendAvailable(true);
        setDbConnected(data.database === "connected");
        if (data.database === "connected") loadHistory();
      } else {
        setBackendAvailable(false);
      }
    } catch (e) {
      setBackendAvailable(false);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await fetch(`${API_URL}/history`);
      if (response.ok) {
        const data = await response.json();
        setHistory(data || []);
      }
    } catch (e) {
      console.error("Failed to load prompt history:", e);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      const reader = new FileReader();
      reader.onload = (event) => setPrompt(event.target.result);
      reader.readAsText(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setFileName(file.name);
      const reader = new FileReader();
      reader.onload = (event) => setPrompt(event.target.result);
      reader.readAsText(file);
    }
  };

  const handleAudit = async (overridePrompt = null, customLoadingMessage = null) => {
    const textToAudit = typeof overridePrompt === 'string' ? overridePrompt : prompt;
    
    if (!textToAudit.trim()) {
      alert("Please enter prompt text first!");
      return;
    }

    if (!backendAvailable) {
      alert("Backend API is currently offline. Cannot evaluate.");
      return;
    }

    setLoadingMessage(customLoadingMessage);
    setIsAuditing(true);
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: textToAudit })
      });
      
      if (response.ok) {
        const data = await response.json();
        setReport(data);
        if (dbConnected) loadHistory();
      } else {
        const err = await response.json();
        alert("Engine error: " + err.detail);
      }
    } catch (e) {
      console.error("Backend error:", e);
      alert("Backend API is unreachable.");
    } finally {
      setIsAuditing(false);
    }
  };

  const handleCopy = () => {
    if (!prompt) return;
    navigator.clipboard.writeText(prompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderPillars = () => {
    if (!report) return null;
    const metrics = report.metrics || {};
    const keys = ["well_structured", "safe", "optimized", "context_rich", "role_specific", "hallucination_resistant", "reusable", "professional"];
    
    return keys.map(k => {
      const metricVal = metrics[k] || { score: 0, status: "fail", feedback: "N/A" };
      let color = "var(--fail-color)";
      if (metricVal.score >= 8) color = "var(--pass-color)";
      else if (metricVal.score >= 5) color = "var(--warn-color)";

      return (
        <div className="pillar-card" key={k}>
          <div className="pillar-header">
            <span className="pillar-name">{k.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('-')}</span>
            <span className="pillar-score" style={{ color }}>{metricVal.score}/10</span>
          </div>
          <div className="pillar-track">
            <div className="pillar-fill" style={{ width: `${metricVal.score * 10}%`, background: color }}></div>
          </div>
          <div className="pillar-feedback">{metricVal.feedback}</div>
        </div>
      );
    });
  };

  const getScoreInfo = () => {
    if (!report) return { score: 0, color: "var(--text-muted)", tier: "", desc: "" };
    const score = report.overall_score || report.scoring?.score || 0;
    if (score >= 80) return { score, color: "var(--pass-color)", tier: "OPTIMIZED", desc: "Excellent technical standard. Structured persona, strong security bounds, and robust reusable attributes are established." };
    if (score >= 60) return { score, color: "var(--warn-color)", tier: "ADEQUATE", desc: "Your prompt meets the baseline standards but possesses significant optimization potential to improve performance." };
    return { score, color: "var(--fail-color)", tier: "SUBOPTIMAL", desc: "The instruction set contains structural gaps and lack of negative guardrails. Highly vulnerable to hallucination." };
  };

  const scoreInfo = getScoreInfo();
  const dashOffset = 283 - (283 * scoreInfo.score) / 100;

  return (
    <div className="app-container">
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div className="logo-container">
            <div className="logo-symbol">F</div>
            <span className="gradient-text">FixForge</span>
          </div>
          <button className="sidebar-toggle-btn" onClick={() => setIsDrawerOpen(true)}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
            Prompt Library
          </button>
          <button className="sidebar-toggle-btn" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} title="Toggle Light/Dark Mode">
            {theme === 'dark' ? (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="4.22" x2="19.78" y2="5.64"></line></svg>
            ) : (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            )}
          </button>
        </div>
        
        <div className={`status-badge ${!backendAvailable ? 'offline' : ''}`}>
          <div className="status-dot"></div>
          <span>{!backendAvailable ? "Backend Offline" : (!dbConnected ? "Database Disconnected" : "Engine Connected")}</span>
        </div>
      </header>

      {/* History Drawer */}
      <div className={`history-drawer ${isDrawerOpen ? 'open' : ''}`}>
        <div className="drawer-header">
          <h3>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path></svg>
            Prompt History
          </h3>
          <button className="close-drawer-btn" onClick={() => setIsDrawerOpen(false)}>&times;</button>
        </div>
        <div className="history-list">
          {history.length === 0 ? (
             <div style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.8rem', padding: '2rem 0' }}>No evaluated prompts yet.</div>
          ) : (
             history.map((item, idx) => {
               const time = new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
               const date = new Date(item.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric' });
               return (
                 <div className="history-card" key={idx} onClick={() => {
                   setPrompt(item.prompt);
                   setReport(item);
                   setIsDrawerOpen(false);
                 }}>
                   <div className="history-card-top">
                     <span className="history-type-badge">{item.prompt_type || 'System Prompt'}</span>
                     <span className="history-score-badge">{item.overall_score || 0}%</span>
                   </div>
                   <div className="history-snippet">{item.prompt}</div>
                   <span className="history-time">{date} @ {time}</span>
                 </div>
               );
             })
          )}
        </div>
      </div>

      <main className="workspace-layout">
        {/* Left Panel - Editor */}
        <section className="glass-panel panel">
          <div className="panel-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
            Workspace
          </div>

          <div 
            className="upload-zone" 
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
          >
            <input type="file" ref={fileInputRef} onChange={handleFileUpload} accept=".txt,.md,.prompt" style={{ display: 'none' }} />
            <svg className="upload-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
            <span>Drag & drop prompt files or <strong>Browse</strong></span>
          </div>

          <div className="editor-container">
            <div className="editor-header">
              <span>RAW PROMPT INPUT</span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span>{prompt.length} chars</span>
                <button 
                  className="sidebar-toggle-btn" 
                  style={{ padding: '0.2rem 0.5rem', border: 'none', background: 'transparent' }}
                  onClick={handleCopy}
                  title="Copy Prompt"
                >
                  {copied ? (
                    <span style={{ color: 'var(--pass-color)', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                      Copied!
                    </span>
                  ) : (
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                  )}
                </button>
              </div>
            </div>
            <textarea 
              value={prompt}
              onChange={(e) => {
                setPrompt(e.target.value);
                setFileName("");
              }}
              placeholder="Enter raw system instructions, role prompts, templates or system configurations to audit..."
            />
          </div>

          <button className="btn" onClick={handleAudit} disabled={isAuditing || !prompt.trim()}>
            {isAuditing ? (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="pulse-icon"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"></path></svg>
                Auditing Quality...
              </>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Evaluate Prompt Quality
              </>
            )}
          </button>

          {report && report.optimization?.improved_prompt && report.optimization.improved_prompt !== prompt && (
            <div className="optimization-preview">
              <div className="optimization-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--pass-color)" strokeWidth="2.5"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path></svg>
                <span className="gradient-text" style={{fontWeight: 800}}>Suggested Optimization</span>
              </div>
              <textarea 
                className="optimized-textarea"
                readOnly
                value={report.optimization.improved_prompt}
              />
              <button 
                className="btn accept-btn" 
                onClick={() => {
                  const newPrompt = report.optimization.improved_prompt;
                  setPrompt(newPrompt);
                  handleAudit(newPrompt, "Forging Your Prompt...");
                }}
                disabled={isAuditing}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                Accept Changes & Re-Evaluate
              </button>
            </div>
          )}
        </section>

        {/* Right Panel - Results */}
        <section className="glass-panel panel" style={{ overflowY: 'auto' }}>
          <div className="panel-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            Diagnostics Hub
          </div>

          {!report ? (
            <div className="results-placeholder">
              <span style={{ fontSize: '3rem' }}>🧠</span>
              <p>Enter your raw instructions on the left workspace and click <strong>Evaluate Prompt Quality</strong> to audit structural rigor, safety metrics, hallucination thresholds, and generate an optimized coach version.</p>
            </div>
          ) : (
            <div className="results-content">
              <div className="score-hub">
                <div className="score-circle">
                  <svg className="score-svg" viewBox="0 0 100 100">
                    <circle className="score-bg" cx="50" cy="50" r="45"></circle>
                    <circle 
                      className="score-active" 
                      cx="50" cy="50" r="45" 
                      style={{ stroke: scoreInfo.color, strokeDasharray: 283, strokeDashoffset: dashOffset }}
                    ></circle>
                  </svg>
                  <div className="score-text">
                    {scoreInfo.score}
                    <span className="score-label">SCORE</span>
                  </div>
                </div>
                <div className="score-info">
                  <h3 style={{ color: scoreInfo.color }}>{scoreInfo.tier}</h3>
                  <p>{scoreInfo.desc}</p>
                </div>
              </div>

              <div>
                <h4 style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Quality Dimensions (8 Core Pillars)</h4>
                <div className="pillars-grid">
                  {renderPillars()}
                </div>
              </div>

              {report.suggestions && report.suggestions.length > 0 && (
                <div className="suggestions-box">
                  <div className="suggestions-title">💡 Actionable Coaching Suggestions</div>
                  <div className="suggestions-list">
                    {report.suggestions.map((s, i) => (
                      <div className="suggestion-item" key={i}>{s}</div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>
      </main>

      {isAuditing && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <h2>{loadingMessage || (fileName ? `Analyzing ${fileName}...` : 'Forging Perfect Prompt...')}</h2>
          <p>Evaluating 8 core quality pillars & generating optimizations</p>
        </div>
      )}
    </div>
  )
}

export default App
