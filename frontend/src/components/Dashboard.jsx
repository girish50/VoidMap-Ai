import React, { useState, useEffect } from 'react';
import { useAnalysisStore } from '../store/useAnalysisStore';
import { 
  FileText, Play, History, ShieldAlert, Cpu, AlertTriangle, 
  HelpCircle, Sliders, RefreshCw, BarChart2, Layers, CheckSquare,
  Activity, Landmark, Terminal, Network, UploadCloud, FileCheck2,
  Download, ShieldAlert as AlertIcon, FileCode, MessageSquare, ChevronDown, ChevronUp
} from 'lucide-react';

import FlowViewer from './FlowViewer';
import ExpertDebate from './ExpertDebate';
import FailureDNAMap from './RadarChart';

const starterTemplates = [
  {
    title: "Healthcare Diagnostic AI",
    subtitle: "FDA/CE regulatory compliance audit for CNN radiological model",
    domain: "Healthcare",
    projectType: "Medical AI",
    riskLevel: "High",
    techInput: "React, FastAPI, PyTorch, Docker",
    userConsidered: ["Validation", "Security"],
    description: "AlphaMed moderate diagnostic model. The system processes chest scans to classify lung pathologies. We have run standard clinical validation against reference datasets and protect patient privacy via standard database encryption. Further bias validation and regulatory paths are pending."
  },
  {
    title: "Startup FinTech Ledger Node",
    subtitle: "Due diligence scalability and risk liability projection",
    domain: "Startup",
    projectType: "FinTech Platform",
    riskLevel: "Medium",
    techInput: "React, FastAPI, PostgreSQL",
    userConsidered: ["Scalability"],
    description: "CloudLedger SaaS platform. Focuses on customer ledger accounts, running simple scaling databases. Transaction logs are encrypted, but multi-region backup structures and database schema migrations have not been detailed. Scaling projections are modelled with linear constraints."
  },
  {
    title: "Zero-Trust Credential Shield",
    subtitle: "Threat modeling and secure credential rotation review",
    domain: "Cybersecurity",
    projectType: "Authentication Core",
    riskLevel: "Critical",
    techInput: "FastAPI, React, Docker, Solidity",
    userConsidered: ["Security", "Compliance"],
    description: "LedgerShield authentication protocol. Uses static API tokens and standard HSM credentials. We assert absolute cryptographic resilience against all zero-day exploit packages. Detailed key rotation processes, STRIDE threat models, and insider threat audit logging are pending final engineering sprints."
  },
  {
    title: "Scientific Research Proposal",
    subtitle: "Ablation and control group validation tracking",
    domain: "Research",
    projectType: "Academic Paper Draft",
    riskLevel: "Low",
    techInput: "Python, NumPy, Jupyter",
    userConsidered: ["Accuracy"],
    description: "We present a neural attention pipeline demonstrating state-of-the-art results on standard benchmarks. Ablation studies isolating sub-layer weights, negative control validation runs, and reproducibility data sharing roadmaps are omitted from this initial draft."
  }
];

export default function Dashboard() {
  const { 
    projects, activeProject, loading, error, theme,
    fetchProjects, fetchProjectDetails, analyzeProposal, recalculateCounterfactual 
  } = useAnalysisStore();

  // Active Workspace Tab: 'new_audit' (Default View), 'dashboard' (Report), 'expectation_graph' (Neo4j Explorer)
  const [activeTab, setActiveTab] = useState('new_audit');

  // Submission Form State
  const [name, setName] = useState('');
  const [domain, setDomain] = useState('Healthcare');
  const [projectType, setProjectType] = useState('');
  const [riskLevel, setRiskLevel] = useState('High');
  const [techInput, setTechInput] = useState('');
  const [description, setDescription] = useState('');
  const [userConsidered, setUserConsidered] = useState([]);
  const [inputMode, setInputMode] = useState('guided'); // 'guided' or 'plaintext'

  // PDF Upload Simulation State
  const [pdfFile, setPdfFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Sliders State for Counterfactual Sandbox
  const [sliderVals, setSliderVals] = useState({});

  // Loading Steps Progressive State
  const [loadingStage, setLoadingStage] = useState(0);

  // Gaps expandable accordion state
  const [expandedGap, setExpandedGap] = useState(null);

  // Counterfactual Scenario Preset state
  const [activeScenario, setActiveScenario] = useState('normal');

  // Startup Seeding
  useEffect(() => {
    fetchProjects();
  }, []);

  // Update local slider inputs and reset preset when a new analysis completes
  useEffect(() => {
    if (activeProject && Array.isArray(activeProject.counterfactuals)) {
      const initialSliders = {};
      activeProject.counterfactuals.forEach(sc => {
        initialSliders[sc.trigger_parameter] = 1.0;
      });
      setSliderVals(initialSliders);
      setActiveScenario('normal');
    }
  }, [activeProject]);

  // Handle Loading progression
  useEffect(() => {
    let interval;
    if (loading) {
      setLoadingStage(1);
      interval = setInterval(() => {
        setLoadingStage((prev) => (prev < 5 ? prev + 1 : 5));
      }, 700);
    } else {
      setLoadingStage(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  // Handle PDF/Document Upload Simulation
  const handlePdfUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPdfFile(file);
    setUploading(true);
    setUploadProgress(0);

    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploading(false);
          
          const lowerName = file.name.toLowerCase();
          if (lowerName.includes('robust') || lowerName.includes('90')) {
            setName("AlphaMed Chest X-Ray CNN [Robust 90%]");
            setDomain("Healthcare");
            setProjectType("Medical AI");
            setTechInput("React, FastAPI, PyTorch, Docker");
            setUserConsidered(["Validation", "Security", "Ethics", "Compliance", "Monitoring"]);
            setDescription("AlphaMed robust diagnostic proposal. We have completed clinical validation trials on independent radiological datasets. Standard patient privacy is enforced with HIPAA-compliant data encryption and automatic demographic bias mitigation across patient age cohorts. We are preparing legal documents for the FDA / CE Regulatory Pathway and have integrated explainability networks providing radiologists with attention heatmap highlights.");
          } else if (lowerName.includes('moderate') || lowerName.includes('70')) {
            setName("AlphaMed Chest X-Ray CNN [Moderate 70%]");
            setDomain("Healthcare");
            setProjectType("Medical AI");
            setTechInput("React, FastAPI, PyTorch, Docker");
            setUserConsidered(["Validation", "Security"]);
            setDescription("AlphaMed moderate diagnostic model. The system processes chest scans to classify lung pathologies. We have run standard clinical validation against reference datasets and protect patient privacy via standard database encryption. Further bias validation and regulatory paths are pending.");
          } else if (lowerName.includes('fragile') || lowerName.includes('40')) {
            setName("AlphaMed Chest X-Ray CNN [Fragile 40%]");
            setDomain("Healthcare");
            setProjectType("Medical AI");
            setTechInput("React, FastAPI, PyTorch");
            setUserConsidered([]);
            setDescription("AlphaMed raw model proposal. We claim this convolutional neural network has absolute 100% unbreakable diagnostic accuracy and runs instantly without lag. It integrates directly with public scanners and works perfectly.");
          } else if (lowerName.includes('medical') || lowerName.includes('health') || lowerName.includes('med')) {
            setName("AlphaMed Chest X-Ray CNN");
            setDomain("Healthcare");
            setProjectType("Medical AI");
            setTechInput("React, FastAPI, PyTorch, Docker");
            setUserConsidered(["Security", "Accuracy", "Deployment", "Compliance", "Validation", "Monitoring"]);
            setDescription("A convolutional neural network model trained on public medical imaging datasets. The system is designed to classify chest X-ray scans for diseases like tuberculosis and pneumonia. It automatically deploys model outputs as attention heatmaps to radiologist terminals.");
          } else if (lowerName.includes('ledger') || lowerName.includes('fintech') || lowerName.includes('security')) {
            setName("Core FinTech Ledger Node");
            setDomain("Cybersecurity");
            setProjectType("Ledger Node");
            setTechInput("FastAPI, React, Docker, Solidity");
            setUserConsidered(["Security", "Deployment", "Compliance", "Ethics"]);
            setDescription("We are launching a completely secure FinTech ledger node utilizing smart contracts. It guarantees 100% unbreakable security for client transactions and will always execute instantly.");
          } else {
            setName(file.name.split('.')[0] + " System");
            setDomain("Startup");
            setProjectType("SaaS Platform");
            setTechInput("React, Node.js, PostgreSQL");
            setUserConsidered(["Scalability", "Ethics"]);
            setDescription(`This technical proposal outlines the deployment parameters of the ${file.name.split('.')[0]} system. The design integrates scalable database components and processes user inputs to generate structured reporting pipelines.`);
          }
          return 100;
        }
        return prev + 20;
      });
    }, 150);
  };

  // Handle factor selection checkboxes
  const handleCheckboxChange = (factor) => {
    if (userConsidered.includes(factor)) {
      setUserConsidered(userConsidered.filter(f => f !== factor));
    } else {
      setUserConsidered([...userConsidered, factor]);
    }
  };

  // Submit Proposal pipeline trigger
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim() || !description.trim()) return;

    const payload = {
      project_name: name,
      domain,
      project_type: projectType || `${domain} System`,
      risk_level: riskLevel,
      tech_stack: techInput ? techInput.split(',').map(t => t.trim()) : [],
      considered_factors: userConsidered,
      proposal_text: description
    };

    try {
      await analyzeProposal(payload);
      setActiveTab('dashboard'); // Switch back to dashboard report instantly
      
      // Clear form inputs
      setName('');
      setProjectType('');
      setTechInput('');
      setDescription('');
      setUserConsidered([]);
      setPdfFile(null);
    } catch (err) {
      console.error(err);
    }
  };

  // Slider change handler with asynchronous recalculation call
  const handleSliderChange = (param, value) => {
    const updatedSliders = { ...sliderVals, [param]: parseFloat(value) };
    setSliderVals(updatedSliders);
    
    if (activeProject) {
      recalculateCounterfactual(activeProject.analysis_id, updatedSliders);
    }
  };

  // Apply scenario trigger pills preset values
  const handleApplyScenario = (scenario) => {
    setActiveScenario(scenario);
    if (!activeProject || !Array.isArray(activeProject.counterfactuals)) return;

    let presets = {};
    activeProject.counterfactuals.forEach(sc => {
      presets[sc.trigger_parameter] = 1.0;
    });

    if (scenario === 'regulation') {
      if ('regulatory_severity' in presets) presets['regulatory_severity'] = 1.8;
      if ('scanner_degradation' in presets) presets['scanner_degradation'] = 1.1;
      if ('insider_vulnerability' in presets) presets['insider_vulnerability'] = 1.4;
    } else if (scenario === 'drift') {
      if ('traffic_surge' in presets) presets['traffic_surge'] = 1.8;
      if ('scanner_degradation' in presets) presets['scanner_degradation'] = 1.8;
      if ('ddos_intensity' in presets) presets['ddos_intensity'] = 1.2;
    } else if (scenario === 'cyberattack') {
      if ('insider_vulnerability' in presets) presets['insider_vulnerability'] = 1.8;
      if ('ddos_intensity' in presets) presets['ddos_intensity'] = 2.0;
      if ('traffic_surge' in presets) presets['traffic_surge'] = 1.3;
    }

    setSliderVals(presets);
    recalculateCounterfactual(activeProject.analysis_id, presets);
  };

  // Load a Starter Template and prefill form inputs
  const handleLoadTemplate = (tpl) => {
    setName(tpl.title);
    setDomain(tpl.domain);
    setProjectType(tpl.projectType);
    setRiskLevel(tpl.riskLevel);
    setTechInput(tpl.techInput);
    setUserConsidered(tpl.userConsidered);
    setDescription(tpl.description);
    setActiveTab('new_audit'); // Redirect to submit terminal
  };

  // Dynamic Markdown Report Generator
  const getAuditReportMarkdown = () => {
    if (!activeProject) return '';

    const projectName = activeProject.name || "VoidMap_Project";
    const projectDomain = activeProject.domain || "General";
    const projectType = activeProject.project_type || "System Spec";
    const riskLevel = activeProject.risk_level || "Medium";

    return `# VOIDMAP AI — COMPREHENSIVE ARCHITECTURAL AUDIT REPORT
======================================================================
Project Identifier: ${projectName}
Target Assessment Domain: ${projectDomain}
Project Sub-Type: ${projectType}
Risk Sensitivity Level: ${riskLevel}
Audited Date: ${new Date().toLocaleDateString()}

======================================================================
1. SYSTEM DEFICIT SUMMARY & METRICS
======================================================================
- BLINDSPOT INDEX (Aggregated Risk): ${activeProject.blindspot_score || 0}%
- DOMAIN EXPECTATION COVERAGE: ${activeProject.coverage_score || 0}%
- PREDICTED MAINTENANCE SCALING OVERHEAD: ${activeProject.predicted_complexity_growth || 0}%
- THREAT CLASSIFICATION (SVC): ${activeProject.threat_profile_class || "Vulnerable"}
- CHAIN FRACTURE PROBABILITY (Logistic Regression): ${Math.round(activeProject.chain_fracture_probability || 50.0)}% (Binary Yes/No Prediction)
- ESTIMATED RISK LIABILITY COST (Linear Regression): ₹${Math.round(activeProject.financial_liability_projection || 500.0)}K (Numerical Prediction)

>>> HAZARD WARNING: Your proposal leaves ${Array.isArray(activeProject.missing_factors) ? activeProject.missing_factors.length : 0} expected requirements completely unaddressed. This fractures the target domain's dependency networks and increases vulnerability to cascading operational collapse.

======================================================================
2. STRUCTURAL BLUEPRINT GAPS (${Array.isArray(activeProject.missing_factors) ? activeProject.missing_factors.length : 0} Critical Voids)
======================================================================
${Array.isArray(activeProject.missing_factors) && activeProject.missing_factors.length > 0 ? activeProject.missing_factors.map((gap, i) => `
[GAP #${i+1}] ${(gap.requirement || "Unspecified").toUpperCase()} (Category: ${gap.category || "General"})
- Description: ${gap.description || "No description provided."}
- Downstream Cascading Hazard: "${gap.risk || "No hazard modeled."}"
- Dependency Constraint: ${gap.fractured_chain ? "FRACTURED (Blocker for other components)" : "Isolated gap"}
`).join('\n') : "No expected blueprint gaps found."}

======================================================================
3. SILENT ASSUMPTIONS STRESS TEST
======================================================================
${Array.isArray(activeProject.assumptions) && activeProject.assumptions.length > 0 ? activeProject.assumptions.map((ass, i) => `
[ASSUMPTION #${i+1}] "${ass.claim || "Unspecified claim"}"
- Assertion Classification: ${ass.type || "General Claim"}
- Fragility Score: ${ass.fragility_score || 5}/10 (Vulnerability: ${ass.vulnerability || "No details modeled."})
- Adversarial Attack Question: "${ass.attack_question || "No stress test question modeled."}"
`).join('\n') : "No implicit assumptions parsed."}

======================================================================
4. DISASTER DNA SIMILARITY ARCHETYPES
======================================================================
${Array.isArray(activeProject.failure_dna) && activeProject.failure_dna.length > 0 ? activeProject.failure_dna.map((fail, i) => `
[COLLAPSE PROXIMITY #${i+1}] ${fail.name || "Historical Case"} (Similarity Match: ${Math.round((fail.similarity || 0) * 100)}%)
- Summary of Failure: ${fail.summary || "No details."}
- Downstream Consequences: ${fail.consequences || "No details."}
- Preventative System Lesson: "${fail.lesson || "No details."}"
`).join('\n') : "No collapse proximity matches modeled."}

======================================================================
5. MULTI-PERSPECTIVE BOARDROOM CRITIQUES
======================================================================
${Array.isArray(activeProject.expert_reviews) && activeProject.expert_reviews.length > 0 ? activeProject.expert_reviews.map((rev, i) => `
- [${(rev.expert_name || "Expert").toUpperCase()} ADVISOR] (Risk Rating: ${rev.rating || 5}/10)
  Feedback: "${rev.critique || rev.review_text || "No feedback logged."}"
`).join('\n') : "No advisor reviews recorded."}

======================================================================
REPORT GENERATED AUTOMATICALLY BY VOIDMAP AI DECISION INTELLIGENCE CORE.
`;
  };

  // Compile Boardroom debate markdown
  const getBoardroomDebateMarkdown = () => {
    if (!activeProject) return '';
    let md = `# BOARDROOM ADVERSARIAL DEBATE TRANSCRIPT\n\n`;
    md += `Project Identifier: ${activeProject.name}\n`;
    md += `Domain: ${activeProject.domain}\n`;
    md += `Date: ${new Date().toLocaleDateString()}\n\n`;
    md += `## 1. Multi-Perspective Expert Reviews\n\n`;
    if (Array.isArray(activeProject.expert_reviews)) {
      activeProject.expert_reviews.forEach(r => {
        md += `### ${r.expert_name} (Rating: ${r.rating}/10)\n`;
        md += `> "${r.critique || r.review_text}"\n\n`;
      });
    }
    md += `## 2. Adversarial Dialogue Clashes\n\n`;
    if (Array.isArray(activeProject.board_disagreements)) {
      activeProject.board_disagreements.forEach(c => {
        md += `### Clash: ${c.clash}\n`;
        md += `Dialogue:\n\`\`\`\n${c.dialogue}\n\`\`\`\n\n`;
      });
    }
    return md;
  };

  const sanitizeFilename = (name) => {
    if (!name) return 'project';
    return name
      .toLowerCase()
      .replace(/[^a-z0-9_-]/g, '_')
      .replace(/_+/g, '_')
      .replace(/^_+|_+$/g, '');
  };

  const downloadReport = () => {
    if (!activeProject) return;
    const content = getAuditReportMarkdown();
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${sanitizeFilename(activeProject.name)}_voidmap_audit_report.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Generate local Neo4j expected requirements graph visualization
  const getExpectationGraphData = () => {
    if (!activeProject || !Array.isArray(activeProject.missing_factors)) return { nodes: [], edges: [] };
    
    const missingSet = new Set(activeProject.missing_factors.map(m => m.requirement));
    
    const domainReqs = {
      "Healthcare": ["Clinical Validation", "Demographic Bias Mitigation", "FDA / CE Regulatory Pathway", "Clinical Drift Monitoring", "Explainability & Interpretability", "Patient Privacy & HIPAA"],
      "Cybersecurity": ["Threat Modeling", "Key Lifecycle Management", "Insider Threat Auditing", "Disaster Recovery Strategy", "Adversarial Robustness Testing"],
      "Startup": ["Regulatory Compliance Analysis", "Customer Acquisition Cost Audit", "Infrastructure Scaling Model", "IP and Patent Strategy", "User Offboarding & Data Deletion"],
      "Research": ["Negative Control Groups", "Reproducibility Roadmap", "Ablation Studies", "Limitations and Scope Disclosure"],
      "Engineering": ["Load Testing & Scalability", "Database Drift & Schema Migrations", "End-to-End Latency Profile", "Secrets and Credentials Shielding"]
    };

    const reqs = domainReqs[activeProject.domain] || ["Clinical Validation", "Threat Modeling", "Regulatory Compliance Analysis"];
    
    const nodes = [
      {
        id: "d1",
        type: "input",
        data: { label: `🕸️ Domain: ${activeProject.domain}` },
        position: { x: 250, y: 20 },
        style: { background: '#8B5CF6', color: '#FFF', border: '1px solid #7C3AED', padding: '10px', borderRadius: '8px' }
      }
    ];

    const edges = [];

    reqs.forEach((r, idx) => {
      const isMissing = missingSet.has(r);
      const xPos = 80 + (idx % 3) * 170;
      const yPos = 140 + Math.floor(idx / 3) * 120;

      nodes.push({
        id: `r-${idx}`,
        data: { label: `${isMissing ? '❌' : '✓'} ${r}` },
        position: { x: xPos, y: yPos },
        style: {
          background: isMissing ? 'rgba(244, 63, 94, 0.05)' : 'rgba(37, 99, 235, 0.05)',
          color: isMissing ? 'var(--brand-danger)' : 'var(--brand-primary)',
          border: isMissing ? '1px solid var(--brand-danger)' : '1px solid var(--brand-primary)',
          padding: '10px',
          borderRadius: '8px',
          fontSize: '11px',
          fontWeight: '550'
        }
      });

      edges.push({
        id: `e-d1-r${idx}`,
        source: "d1",
        target: `r-${idx}`,
        animated: isMissing
      });
    });

    return { nodes, edges };
  };

  const getBlindspotBadgeColor = (score) => {
    if (score >= 70) return 'text-brand-danger bg-brand-danger/10 border-brand-danger/25';
    if (score >= 40) return 'text-brand-warning bg-brand-warning/10 border-brand-warning/25';
    return 'text-brand-primary bg-brand-primary/10 border-brand-primary/25';
  };

  const domainOptions = ['Healthcare', 'Cybersecurity', 'Startup', 'Research', 'Engineering', 'Finance', 'Policy'];
  const checkboxOptions = ['Security', 'Accuracy', 'Deployment', 'Scalability', 'Compliance', 'Validation', 'Monitoring', 'Ethics'];

  // Calculate circular progress indicator metrics
  const getStrokeDashoffset = (percent, radius = 45) => {
    const circumference = 2 * Math.PI * radius;
    return circumference - (percent / 100) * circumference;
  };

  // Convert stage integer to visual text for the AI Status Rail
  const getLoadingStageText = () => {
    switch (loadingStage) {
      case 1: return "Semantic Parsing...";
      case 2: return "Neo4j Mapping...";
      case 3: return "Failure DNA Matching...";
      case 4: return "Boardroom Synthesis...";
      case 5: return "Fitting ML Regressors...";
      default: return "Analyzing...";
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 transition-colors duration-300">
      
      {/* COBALT TITLE BANNER */}
      <div className="flex items-center justify-between border-b border-border-color pb-5 mb-8">
        <div>
          <h1 className="text-2xl font-extrabold bg-gradient-to-r from-brand-primary to-brand-purple bg-clip-text text-transparent tracking-wide uppercase void-glow">
            VOIDMAP AI reasoning terminal
          </h1>
          <p className="text-xs text-text-muted mt-1 leading-relaxed">
            Stress-testing system designs, startup plans, and architectures for unmodeled hazards.
          </p>
        </div>
        
        {/* Subtle AI Status Rail & DB Indicators */}
        <div className="flex items-center space-x-2">
          {loading ? (
            <div className="flex items-center space-x-2 px-3.5 py-1.5 bg-brand-primary/10 border border-brand-primary/20 rounded-full text-[10px] text-brand-primary font-mono font-bold uppercase tracking-wider animate-pulse">
              <span className="w-1.5 h-1.5 bg-brand-primary rounded-full animate-ping" />
              <span>AI Rails: {getLoadingStageText()}</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1.5 px-3.5 py-1.5 bg-card border border-border-color rounded-full text-[10px] text-text-muted font-mono font-bold uppercase tracking-wider">
              <Activity className="w-3.5 h-3.5 text-brand-success mr-1.5 animate-pulse" />
              <span>AI Rails: Idle</span>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
        
        {/* ==================================================== */}
        {/* COLUMN 1: SIDEBAR HISTORY REGISTRY (PLACED AT LEFT) */}
        {/* ==================================================== */}
        <div className="xl:col-span-1 space-y-6">
          
          {/* Historical Session Card */}
          <div className="glass-card p-5 relative overflow-hidden bg-card border border-border-color">
            
            {/* Background glowing indicator */}
            <div className="absolute top-0 right-0 w-24 h-24 bg-brand-primary/5 rounded-full blur-2xl -mr-4 -mt-4" />

            <h3 className="font-extrabold text-xs text-text-main tracking-widest uppercase mb-4 flex items-center space-x-2 border-b border-border-color pb-3">
              <History className="w-4 h-4 text-brand-primary" />
              <span>Historical ledger</span>
            </h3>
            
            {projects.length === 0 ? (
              <p className="text-xs text-text-muted py-2 leading-relaxed">No past analyses found. Load a template or initialize your first audit.</p>
            ) : (
              <div className="space-y-2 max-h-[480px] overflow-y-auto pr-1">
                {projects.map((proj) => {
                  const isActive = activeProject && activeProject.project_id === proj.id;
                  return (
                    <button
                      key={proj.id}
                      onClick={() => {
                        fetchProjectDetails(proj.id);
                        setActiveTab('dashboard'); // Auto redirect to dashboard view
                      }}
                      className={`w-full text-left p-3.5 rounded-xl border text-xs transition-all duration-300 relative group overflow-hidden cursor-pointer ${
                        isActive
                          ? 'border-brand-purple bg-brand-purple/5 ring-1 ring-brand-purple/10'
                          : 'border-border-color bg-bg/40 hover:border-brand-purple/35'
                      }`}
                    >
                      {/* Hover Glow Accent */}
                      <div className="absolute top-0 left-0 w-0.5 h-full bg-brand-purple opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      
                      <div className="font-bold text-text-main truncate mb-1 pr-6">{proj.name}</div>
                      <div className="flex items-center justify-between mt-1.5 text-[9px] text-text-muted font-bold uppercase tracking-widest">
                        <span>{proj.domain}</span>
                        <span className={`px-1.5 py-0.5 rounded border font-mono font-extrabold ${
                          proj.blindspot_score >= 70 ? 'border-brand-danger/30 text-brand-danger bg-brand-danger/5' : 
                          proj.blindspot_score >= 40 ? 'border-brand-warning/30 text-brand-warning bg-brand-warning/5' : 'border-brand-primary/30 text-brand-primary bg-brand-primary/5'
                        }`}>
                          {proj.blindspot_score}% RISK
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* System Performance Diagnostics */}
          <div className="glass-card p-5 text-[11px] space-y-3 font-mono text-text-muted bg-card border border-border-color">
            <h4 className="font-extrabold text-[10px] text-text-main tracking-widest uppercase mb-1 flex items-center space-x-1.5">
              <Activity className="w-3.5 h-3.5 text-brand-success" />
              <span>System Diagnostics</span>
            </h4>
            <div className="flex justify-between border-b border-border-color/40 pb-1.5">
              <span>Relational (Postgres):</span>
              <span className="text-brand-cyan font-semibold">Active</span>
            </div>
            <div className="flex justify-between border-b border-border-color/40 pb-1.5">
              <span>Graph (Neo4j Aura):</span>
              <span className="text-brand-cyan font-semibold">Active</span>
            </div>
            <div className="flex justify-between">
              <span>Analytics Models:</span>
              <span className="text-brand-success font-semibold">Loaded</span>
            </div>
          </div>

        </div>

        {/* ==================================================== */}
        {/* COLUMNS 2-4: MAIN WORKSPACE COMMAND CENTER */}
        {/* ==================================================== */}
        <div className="xl:col-span-3 space-y-6">

          {/* MASTER TAB NAVIGATION SYSTEM */}
          <div className="flex flex-wrap gap-2 border-b border-border-color pb-3 text-xs font-bold uppercase tracking-wider">
            
            <button
              onClick={() => setActiveTab('new_audit')}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg border transition-all duration-300 cursor-pointer ${
                activeTab === 'new_audit'
                  ? 'border-brand-purple bg-brand-purple/10 text-text-main shadow-glow'
                  : 'border-border-color bg-card text-text-muted hover:border-border-color/80'
              }`}
            >
              <Terminal className="w-4 h-4" />
              <span>🌌 Submit Proposal Terminal</span>
            </button>

            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg border transition-all duration-300 cursor-pointer ${
                activeTab === 'dashboard'
                  ? 'border-brand-purple bg-brand-purple/10 text-text-main shadow-glow'
                  : 'border-border-color bg-card text-text-muted hover:border-border-color/80'
              }`}
            >
              <BarChart2 className="w-4 h-4" />
              <span>📊 Analysis Dashboard</span>
            </button>

            <button
              onClick={() => setActiveTab('expectation_graph')}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg border transition-all duration-300 cursor-pointer ${
                activeTab === 'expectation_graph'
                  ? 'border-brand-purple bg-brand-purple/10 text-text-main shadow-glow'
                  : 'border-border-color bg-card text-text-muted hover:border-border-color/80'
              }`}
            >
              <Network className="w-4 h-4" />
              <span>🕸️ Neo4j Expectation Graph</span>
            </button>
          </div>

          {/* ==================================================== */}
          {/* TAB 1: PROPOSAL TERMINAL FORM (DEFAULT FIRST TAB) */}
          {/* ==================================================== */}
          {activeTab === 'new_audit' && (
            <div className="glass-card p-6 bg-card border border-border-color animate-fade-in space-y-6">
              <h3 className="font-extrabold text-sm text-text-main tracking-widest uppercase flex items-center space-x-2 border-b border-border-color pb-3">
                <FileText className="w-4.5 h-4.5 text-brand-purple" />
                <span>Initiate Adaptive Unknown-Unknown Discovery Audit</span>
              </h3>

              {/* Input Mode Selector Toggle */}
              <div className="flex items-center space-x-2 border-b border-border-color/60 pb-4 text-xs font-bold uppercase tracking-wider">
                <span className="text-[10px] text-text-muted mr-3">Input Mode:</span>
                <button
                  type="button"
                  onClick={() => setInputMode('guided')}
                  className={`px-3 py-1.5 rounded border transition-all duration-200 cursor-pointer ${
                    inputMode === 'guided'
                      ? 'border-brand-primary bg-brand-primary/10 text-brand-primary font-black shadow-sm'
                      : 'border-border-color bg-bg text-text-muted hover:border-border-color/85'
                  }`}
                >
                  📋 Guided Form Mode
                </button>
                <button
                  type="button"
                  onClick={() => setInputMode('plaintext')}
                  className={`px-3 py-1.5 rounded border transition-all duration-200 cursor-pointer ${
                    inputMode === 'plaintext'
                      ? 'border-brand-primary bg-brand-primary/10 text-brand-primary font-black shadow-sm'
                      : 'border-border-color bg-bg text-text-muted hover:border-border-color/85'
                  }`}
                >
                  ✍️ Plain Text Terminal
                </button>
              </div>

              {inputMode === 'guided' ? (
                /* DUAL MANUAL INPUT OPTIONS: DIRECT TEXT AND FILE/PDF UPLOADER */
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  
                  {/* PDF/DOCUMENT UPLOAD WIDGET (LEFT COLUMN) */}
                  <div className="lg:col-span-1 flex flex-col justify-between p-5 bg-bg border border-border-color rounded-xl relative overflow-hidden group">
                    <div>
                      <h4 className="font-bold text-xs text-text-main uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                        <UploadCloud className="w-4 h-4 text-brand-purple" />
                        <span>Document / PDF Uploader</span>
                      </h4>
                      <p className="text-[10px] text-text-muted leading-relaxed mb-4">
                        Drag-and-drop or upload a PDF proposal. The engine simulates direct OCR content extraction instantly.
                      </p>
                    </div>

                    {/* Uploader click block */}
                    <label className="border border-dashed border-border-color hover:border-brand-purple/50 bg-card/60 hover:bg-card p-6 rounded-lg text-center flex flex-col items-center justify-center cursor-pointer transition-all duration-300">
                      <input 
                        type="file" 
                        accept=".pdf,.txt,.docx"
                        onChange={handlePdfUpload}
                        className="hidden" 
                      />
                      
                      {pdfFile ? (
                        <div className="space-y-2">
                          <FileCheck2 className="w-8 h-8 text-brand-cyan mx-auto animate-bounce" />
                          <span className="text-[10px] text-text-main font-bold block truncate max-w-[150px]">{pdfFile.name}</span>
                          <span className="text-[8px] text-text-muted font-mono uppercase block">{Math.round(pdfFile.size/1024)} KB</span>
                        </div>
                      ) : (
                        <div className="space-y-1">
                          <UploadCloud className="w-7 h-7 text-text-muted mx-auto group-hover:text-brand-purple transition-colors" />
                          <span className="text-[10px] text-text-main font-bold block">Choose PDF / Document</span>
                          <span className="text-[8px] text-text-muted block font-mono">PDF, TXT, DOCX</span>
                        </div>
                      )}
                    </label>

                    {/* OCR Extraction Progress Bar */}
                    {uploading && (
                      <div className="mt-4 space-y-1 bg-bg p-3 border border-border-color rounded-lg">
                        <div className="flex justify-between text-[8px] font-mono text-text-muted font-bold">
                          <span>EXTRACTING OCR TEXT...</span>
                          <span>{uploadProgress}%</span>
                        </div>
                        <div className="w-full bg-card h-1.5 rounded-full overflow-hidden">
                          <div 
                            className="bg-gradient-to-r from-brand-primary to-brand-purple h-full transition-all duration-200"
                            style={{ width: `${uploadProgress}%` }}
                          />
                        </div>
                      </div>
                    )}
                  </div>

                  {/* FORM FIELDS (RIGHT COLUMNS) */}
                  <div className="lg:col-span-2 space-y-4">
                    <form onSubmit={handleSubmit} className="space-y-5 text-xs">
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        
                        {/* Project Title */}
                        <div className="flex flex-col space-y-1.5">
                          <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Project Identifier / Name</label>
                          <input
                            type="text"
                            required
                            placeholder="e.g. AI Cardiology Cloud Core"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="bg-bg border border-border-color rounded-lg p-3 text-text-main glow-border w-full font-medium"
                          />
                        </div>

                        {/* Domain Selector */}
                        <div className="flex flex-col space-y-1.5">
                          <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Target Assessment Domain</label>
                          <select
                            value={domain}
                            onChange={(e) => setDomain(e.target.value)}
                            className="bg-bg border border-border-color rounded-lg p-3 text-text-main glow-border w-full cursor-pointer font-medium"
                          >
                            {domainOptions.map(opt => (
                              <option key={opt} value={opt}>{opt}</option>
                            ))}
                          </select>
                        </div>

                        {/* Subsystem / Tech Specs */}
                        <div className="flex flex-col space-y-1.5">
                          <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Tech Stack (Comma Separated)</label>
                          <input
                            type="text"
                            placeholder="e.g. React, FastAPI, PyTorch, Neo4j"
                            value={techInput}
                            onChange={(e) => setTechInput(e.target.value)}
                            className="bg-bg border border-border-color rounded-lg p-3 text-text-main glow-border w-full font-medium"
                          />
                        </div>

                        {/* Risk Level */}
                        <div className="flex flex-col space-y-1.5">
                          <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Project Risk Sensitivity</label>
                          <select
                            value={riskLevel}
                            onChange={(e) => setRiskLevel(e.target.value)}
                            className="bg-bg border border-border-color rounded-lg p-3 text-text-main glow-border w-full cursor-pointer font-medium"
                          >
                            <option value="Low">Low Risk</option>
                            <option value="Medium">Medium Risk</option>
                            <option value="High">High Risk</option>
                            <option value="Critical">Critical Risk</option>
                          </select>
                        </div>

                      </div>

                      {/* Factors Considered Checklist */}
                      <div className="flex flex-col space-y-2">
                        <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Check Factors You HAVE Actively Documented & Mitigated:</label>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-bg/40 p-4 border border-border-color rounded-lg">
                          {checkboxOptions.map((factor) => (
                            <label 
                              key={factor} 
                              className={`flex items-center space-x-2.5 p-2 rounded-md border cursor-pointer select-none transition-all duration-200 ${
                                userConsidered.includes(factor)
                                  ? 'border-brand-purple bg-brand-purple/5 text-text-main'
                                  : 'border-border-color bg-bg/30 text-text-muted hover:border-border-color/80'
                              }`}
                            >
                              <input
                                type="checkbox"
                                checked={userConsidered.includes(factor)}
                                onChange={() => handleCheckboxChange(factor)}
                                className="hidden"
                              />
                              <CheckSquare className={`w-4 h-4 ${userConsidered.includes(factor) ? 'text-brand-purple' : 'text-text-muted'}`} />
                              <span className="text-[11px] font-semibold">{factor}</span>
                            </label>
                          ))}
                        </div>
                      </div>

                      {/* Proposal Text Corpus */}
                      <div className="flex flex-col space-y-1.5">
                        <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Project Proposal Text / Technical Specifications</label>
                        <textarea
                          required
                          rows={5}
                          placeholder="Provide a detailed description of your architectural designs, training datasets, deployment configurations, and data pipeline processes. The Absence Engine will parse this text to determine missing requirements..."
                          value={description}
                          onChange={(e) => setDescription(e.target.value)}
                          className="bg-bg border border-border-color rounded-lg p-3.5 text-text-main glow-border w-full leading-relaxed font-medium"
                        />
                      </div>

                      {/* Submit Trigger */}
                      <div className="flex justify-end pt-2">
                        <button
                          type="submit"
                          disabled={loading}
                          className="px-6 py-3 rounded-lg bg-gradient-to-r from-brand-primary to-brand-purple hover:opacity-90 font-bold uppercase tracking-wider text-[10px] flex items-center space-x-2 shadow-lg disabled:opacity-50 text-white cursor-pointer"
                        >
                          {loading ? (
                            <>
                              <RefreshCw className="w-4 h-4 animate-spin" />
                              <span>Auditing Architecture...</span>
                            </>
                          ) : (
                            <>
                              <Play className="w-4 h-4" />
                              <span>Execute Audit Run</span>
                            </>
                          )}
                        </button>
                      </div>

                    </form>
                  </div>

                </div>
              ) : (
                /* SIMPLIFIED PLAIN TEXT SUBMISSION FORM */
                <div className="p-5 bg-bg/50 border border-border-color rounded-xl">
                  <form onSubmit={handleSubmit} className="space-y-5 text-xs">
                    <h4 className="font-bold text-xs text-text-main uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <FileText className="w-4 h-4 text-brand-purple" />
                      <span>Plain Text Specification Analyzer</span>
                    </h4>
                    <p className="text-[10px] text-text-muted leading-relaxed mb-4">
                      Enter the name of your system and paste a raw specification paragraph. The Absence Engine will parse the paragraph directly to calculate security and compliance gaps.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Project Name */}
                      <div className="flex flex-col space-y-1.5">
                        <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Project Identifier / Name</label>
                        <input
                          type="text"
                          required
                          placeholder="e.g. AI Cardiology Cloud Core"
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          className="bg-bg border border-border-color rounded-lg p-3 text-text-main glow-border w-full font-medium"
                        />
                      </div>

                      {/* Domain Selector */}
                      <div className="flex flex-col space-y-1.5">
                        <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Target Assessment Domain</label>
                        <select
                          value={domain}
                          onChange={(e) => setDomain(e.target.value)}
                          className="bg-bg border border-border-color rounded-lg p-3 text-text-main glow-border w-full cursor-pointer font-medium"
                        >
                          {domainOptions.map(opt => (
                            <option key={opt} value={opt}>{opt}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    {/* Paragraph specifications Textarea */}
                    <div className="flex flex-col space-y-1.5">
                      <label className="text-text-muted font-bold uppercase tracking-widest text-[9px]">Project Proposal Text / Technical Specifications Paragraph</label>
                      <textarea
                        required
                        rows={6}
                        placeholder="Provide a detailed description of your architectural designs, training datasets, deployment configurations, and data pipeline processes. The Absence Engine will parse this text to determine missing requirements..."
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="bg-bg border border-border-color rounded-lg p-3.5 text-text-main glow-border w-full leading-relaxed font-medium"
                      />
                    </div>

                    {/* Submit Button */}
                    <div className="flex justify-end pt-2">
                      <button
                        type="submit"
                        disabled={loading}
                        className="px-6 py-3 rounded-lg bg-gradient-to-r from-brand-primary to-brand-purple hover:opacity-90 font-bold uppercase tracking-wider text-[10px] flex items-center space-x-2 shadow-lg disabled:opacity-50 text-white cursor-pointer"
                      >
                        {loading ? (
                          <>
                            <RefreshCw className="w-4 h-4 animate-spin" />
                            <span>Auditing Plain Text Proposal...</span>
                          </>
                        ) : (
                          <>
                            <Play className="w-4 h-4" />
                            <span>Analyze Plain Text Proposal</span>
                          </>
                        )}
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>
          )}

          {/* ==================================================== */}
          {/* TAB 2: ANALYSIS DASHBOARD */}
          {/* ==================================================== */}
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              
              {/* SKELETON LOADER / PROGRESSIVE REVEAL */}
              {loading && (
                <div className="space-y-6 animate-pulse">
                  {/* Intelligence cards panel */}
                  <div className="glass-card p-5 bg-card border border-border-color mb-6">
                    <h3 className="text-xs font-black text-text-main tracking-widest uppercase mb-4">Absence Engine Rails Progression</h3>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      
                      {/* Context */}
                      <div className={`p-4 border rounded-xl transition-all duration-300 ${
                        loadingStage >= 1 ? 'border-brand-primary/30 bg-brand-primary/5' : 'border-border-color bg-bg opacity-40'
                      }`}>
                        <span className="text-[8px] font-mono text-text-muted block uppercase">Stage 01</span>
                        <h4 className="text-xs font-bold text-text-main mt-1 uppercase">Understanding Context</h4>
                        <p className="text-[10px] text-text-muted mt-1 leading-snug">
                          {loadingStage === 1 ? 'Active (Scanning domains ∙∙∙)' : loadingStage > 1 ? 'Completed' : 'Awaiting start'}
                        </p>
                      </div>

                      {/* Mapping */}
                      <div className={`p-4 border rounded-xl transition-all duration-300 ${
                        loadingStage >= 2 ? 'border-brand-primary/30 bg-brand-primary/5' : 'border-border-color bg-bg opacity-40'
                      }`}>
                        <span className="text-[8px] font-mono text-text-muted block uppercase">Stage 02</span>
                        <h4 className="text-xs font-bold text-text-main mt-1 uppercase">Dependency Mapping</h4>
                        <p className="text-[10px] text-text-muted mt-1 leading-snug">
                          {loadingStage === 2 ? 'Running (Neo4j Cypher query ∙∙∙)' : loadingStage > 2 ? 'Completed (Gaps identified)' : 'Pending'}
                        </p>
                      </div>

                      {/* Discovery */}
                      <div className={`p-4 border rounded-xl transition-all duration-300 ${
                        loadingStage >= 3 ? 'border-brand-primary/30 bg-brand-primary/5' : 'border-border-color bg-bg opacity-40'
                      }`}>
                        <span className="text-[8px] font-mono text-text-muted block uppercase">Stage 03</span>
                        <h4 className="text-xs font-bold text-text-main mt-1 uppercase">Expert Reasoning</h4>
                        <p className="text-[10px] text-text-muted mt-1 leading-snug">
                          {loadingStage === 3 ? 'Analyzing (Adversarial simulation ∙∙∙)' : loadingStage === 4 ? 'Modeling (Scikit regressors ∙∙∙)' : loadingStage > 4 ? 'Completed' : 'Pending'}
                        </p>
                      </div>

                    </div>
                  </div>

                  {/* SKELETON KPI PANEL */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="glass-card p-6 h-28 bg-card border-border-color flex items-center justify-between">
                      <div className="space-y-3 w-1/2">
                        <div className="h-3 bg-border-color rounded w-3/4"></div>
                        <div className="h-5 bg-border-color rounded w-1/2"></div>
                      </div>
                      <div className="w-12 h-12 rounded-full bg-bg"></div>
                    </div>
                    <div className="glass-card p-6 h-28 bg-card border-border-color flex items-center justify-between">
                      <div className="space-y-3 w-1/2">
                        <div className="h-3 bg-border-color rounded w-3/4"></div>
                        <div className="h-5 bg-border-color rounded w-1/2"></div>
                      </div>
                      <div className="w-12 h-12 rounded-full bg-bg"></div>
                    </div>
                    <div className="glass-card p-6 h-28 bg-card border-border-color flex items-center justify-between">
                      <div className="space-y-3 w-1/2">
                        <div className="h-3 bg-border-color rounded w-3/4"></div>
                        <div className="h-5 bg-border-color rounded w-1/2"></div>
                      </div>
                      <div className="w-12 h-12 rounded-full bg-bg"></div>
                    </div>
                  </div>

                  {/* SKELETON DISCOVERY SHEET */}
                  <div className="glass-card p-5 h-48 bg-card border-border-color">
                    <div className="h-3 bg-border-color rounded w-1/4 mb-4"></div>
                    <div className="space-y-3">
                      <div className="h-10 bg-border-color rounded"></div>
                      <div className="h-10 bg-border-color rounded"></div>
                    </div>
                  </div>
                </div>
              )}

              {/* EMPTY STATE - STARTER TEMPLATES GRID */}
              {!loading && !activeProject && (
                <div className="space-y-6 animate-fade-in">
                  <div className="glass-card p-8 bg-card border border-border-color text-center space-y-4">
                    <div className="max-w-xl mx-auto space-y-2">
                      <h3 className="text-base font-black text-text-main uppercase tracking-wider">Workspace Reasoning Terminal</h3>
                      <p className="text-xs text-text-muted">
                        No active audit proposal selected. Select a starter template below to load pre-configured schemas, or click on an entry in the historical ledger registry to view it.
                      </p>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto pt-4">
                      {starterTemplates.map((tpl, i) => (
                        <div 
                          key={i}
                          onClick={() => handleLoadTemplate(tpl)}
                          className="border border-border-color bg-bg p-5 rounded-xl text-left cursor-pointer hover:border-brand-primary/50 transition-all duration-200 group relative overflow-hidden shadow-sm"
                        >
                          <div className="absolute top-0 right-0 w-20 h-20 bg-brand-primary/5 rounded-full blur-xl group-hover:bg-brand-primary/10 transition-colors" />
                          <h4 className="text-xs font-black text-text-main uppercase tracking-wide group-hover:text-brand-primary transition-colors">
                            {tpl.title}
                          </h4>
                          <p className="text-[10px] text-text-muted mt-1 leading-relaxed">
                            {tpl.subtitle}
                          </p>
                          <div className="flex items-center space-x-2 mt-4 text-[9px] font-mono text-text-muted">
                            <span className="bg-card border border-border-color px-2 py-0.5 rounded font-bold text-text-main">{tpl.domain}</span>
                            <span>•</span>
                            <span>{tpl.projectType}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* RENDER ACTIVE AUDIT REPORT DETAILS */}
              {!loading && activeProject && (
                <div className="space-y-6 animate-fade-in">
                  
                  {/* Dynamic KPI Header & Download Button */}
                  <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-border-color pb-5 space-y-3 md:space-y-0">
                    <div>
                      <h2 className="text-xl font-extrabold text-text-main tracking-wide">{activeProject.name}</h2>
                      <span className="text-[10px] text-brand-purple font-mono uppercase tracking-widest mt-1.5 inline-block">
                        Assessment domain: {activeProject.domain} • Sub-Type: {activeProject.project_type}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <span className={`px-3.5 py-1.5 rounded-full border text-[9px] font-extrabold uppercase tracking-widest font-mono ${getBlindspotBadgeColor(activeProject.blindspot_score)}`}>
                        Aggregated Risk: {activeProject.blindspot_score >= 70 ? 'High' : activeProject.blindspot_score >= 40 ? 'Moderate' : 'Low'}
                      </span>
                      
                      <button
                        onClick={downloadReport}
                        className="px-4 py-2.5 rounded-lg bg-gradient-to-r from-brand-primary to-brand-purple hover:opacity-90 font-black uppercase tracking-wider text-[9px] text-white flex items-center space-x-2 shadow-md transition-all duration-300 cursor-pointer"
                      >
                        <Download className="w-3.5 h-3.5 animate-bounce" />
                        <span>Download Audit Report</span>
                      </button>
                    </div>
                  </div>

                  {/* VISUAL "WOW" SYSTEM DEFICIT ALERT PANEL (LACKING DIMENSIONS WARNING) */}
                  <div className="p-5 border border-brand-danger/30 bg-gradient-to-r from-brand-danger/5 to-transparent bg-card rounded-2xl relative overflow-hidden flex items-start space-x-4 shadow-sm">
                    
                    {/* Pulsing warning backdrop */}
                    <div className="absolute top-0 right-0 w-32 h-32 bg-brand-danger/5 rounded-full blur-3xl" />
                    
                    <div className="p-3 bg-brand-danger/10 border border-brand-danger/25 rounded-xl shrink-0">
                      <AlertIcon className="w-6 h-6 text-brand-danger animate-pulse" />
                    </div>
                    
                    <div className="space-y-1 text-xs">
                      <h3 className="text-sm font-black text-brand-danger uppercase tracking-wider">
                        CRITICAL SPECIFICATION VOIDS DETECTED
                      </h3>
                      <p className="text-text-muted leading-relaxed">
                        Your system architecture leaves <strong className="text-brand-danger font-bold underline font-mono">{activeProject.missing_factors.length} expected requirements</strong> completely unconsidered. This fractures your target domain's dependency layers and increases your overall **Blindspot Index** liability score. Resolving these voids will lower your risk exposure by **{(activeProject.missing_factors.length * 9.5).toFixed(1)}%**.
                      </p>
                    </div>
                  </div>

                  {/* KPI STATS CARD GRID (HIGH-TECH RADAR CIRCLES) */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
                    
                    {/* Score 1: Blindspot Score Circle */}
                    <div className="glass-card p-6 bg-card border border-border-color flex items-center justify-between">
                      <div className="space-y-1.5 max-w-[55%]">
                        <span className="text-[9px] text-brand-danger font-extrabold uppercase tracking-widest block">
                          Blindspot Index <span className="text-text-muted text-[8px] tracking-wide block font-mono font-semibold">[Engine: RandomForest]</span>
                        </span>
                        <h4 className="text-xl font-black text-text-main tracking-tight">System Risk</h4>
                        <p className="text-[9px] text-text-muted leading-snug">Aggregate vulnerability rating due to baseline blueprint omissions.</p>
                      </div>

                      {/* SVG Gauge */}
                      <div className="relative w-24 h-24 flex items-center justify-center shrink-0 select-none">
                        <svg className="w-full h-full transform -rotate-90">
                          <circle cx="48" cy="48" r="40" stroke="var(--border-color)" strokeWidth="6" fill="transparent" />
                          <circle 
                            cx="48" cy="48" r="40" 
                            stroke="var(--brand-danger)" strokeWidth="6" fill="transparent" 
                            strokeDasharray={2 * Math.PI * 40}
                            strokeDashoffset={getStrokeDashoffset(activeProject.blindspot_score, 40)}
                            strokeLinecap="round"
                            className="transition-all duration-500 void-glow"
                          />
                        </svg>
                        <span className="absolute font-mono text-base font-black text-brand-danger">{activeProject.blindspot_score}%</span>
                      </div>
                    </div>

                    {/* Score 2: Coverage Score Circle */}
                    <div className="glass-card p-6 bg-card border border-border-color flex items-center justify-between">
                      <div className="space-y-1.5 max-w-[55%]">
                        <span className="text-[9px] text-brand-cyan font-extrabold uppercase tracking-widest block">
                          Expectations Coverage <span className="text-text-muted text-[8px] tracking-wide block font-mono font-semibold">[Engine: Cypher Graph Set-Diff]</span>
                        </span>
                        <h4 className="text-xl font-black text-text-main tracking-tight">Dimensions</h4>
                        <p className="text-[9px] text-text-muted leading-snug">Percentage of baseline domain checks satisfied by your design.</p>
                      </div>

                      {/* SVG Gauge */}
                      <div className="relative w-24 h-24 flex items-center justify-center shrink-0 select-none">
                        <svg className="w-full h-full transform -rotate-90">
                          <circle cx="48" cy="48" r="40" stroke="var(--border-color)" strokeWidth="6" fill="transparent" />
                          <circle 
                            cx="48" cy="48" r="40" 
                            stroke="var(--brand-primary)" strokeWidth="6" fill="transparent" 
                            strokeDasharray={2 * Math.PI * 40}
                            strokeDashoffset={getStrokeDashoffset(activeProject.coverage_score, 40)}
                            strokeLinecap="round"
                            className="transition-all duration-500 void-glow"
                          />
                        </svg>
                        <span className="absolute font-mono text-base font-black text-brand-primary">{activeProject.coverage_score}%</span>
                      </div>
                    </div>

                    {/* Score 3: Complexity Growth Circle */}
                    <div className="glass-card p-6 bg-card border border-border-color flex items-center justify-between">
                      <div className="space-y-1.5 max-w-[55%]">
                        <span className="text-[9px] text-brand-purple font-extrabold uppercase tracking-widest block">
                          Maintenance Growth <span className="text-text-muted text-[8px] tracking-wide block font-mono font-semibold">[Engine: DecisionTree]</span>
                        </span>
                        <h4 className="text-xl font-black text-text-main tracking-tight">Complexity</h4>
                        <p className="text-[9px] text-text-muted leading-snug">Predicted operational scale-up overhead computed via Decision Trees.</p>
                      </div>

                      {/* SVG Gauge */}
                      <div className="relative w-24 h-24 flex items-center justify-center shrink-0 select-none">
                        <svg className="w-full h-full transform -rotate-90">
                          <circle cx="48" cy="48" r="40" stroke="var(--border-color)" strokeWidth="6" fill="transparent" />
                          <circle 
                            cx="48" cy="48" r="40" 
                            stroke="var(--brand-purple)" strokeWidth="6" fill="transparent" 
                            strokeDasharray={2 * Math.PI * 40}
                            strokeDashoffset={getStrokeDashoffset(activeProject.predicted_complexity_growth || 68, 40)}
                            strokeLinecap="round"
                            className="transition-all duration-500 void-glow"
                          />
                        </svg>
                        <span className="absolute font-mono text-base font-black text-brand-purple">
                          {activeProject.predicted_complexity_growth ? `${activeProject.predicted_complexity_growth}%` : '68%'}
                        </span>
                      </div>
                    </div>

                  </div>

                  {/* SECOND ROW MACHINE LEARNING PREDICTIVE SUITE */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    
                    {/* Score 4: Threat Profile SVM Classification */}
                    <div className="glass-card p-6 bg-card border border-border-color flex items-center justify-between">
                      <div className="space-y-1.5 max-w-[55%]">
                        <span className="text-[9px] text-brand-purple font-extrabold uppercase tracking-widest block">
                          Threat Classification <span className="text-brand-purple text-[8px] tracking-wide block font-mono font-semibold">[Engine: SVM Classifier]</span>
                        </span>
                        <h4 className="text-xl font-black text-text-main tracking-tight">Threat Profile</h4>
                        <p className="text-[9px] text-text-muted leading-snug">Linguistic & structural vectors mapped to boundary threat classes.</p>
                      </div>

                      {/* SVG Status Gauge */}
                      <div className="relative w-24 h-24 flex flex-col items-center justify-center shrink-0 border border-border-color bg-bg rounded-xl select-none">
                        <span className={`text-[10px] font-mono uppercase font-black tracking-widest px-2 py-1 rounded border ${
                          activeProject.threat_profile_class === 'Critical' ? 'border-brand-danger/30 text-brand-danger bg-brand-danger/5' :
                          activeProject.threat_profile_class === 'Vulnerable' ? 'border-brand-warning/30 text-brand-warning bg-brand-warning/5' : 'border-brand-success/30 text-brand-success bg-brand-success/5'
                        }`}>
                          {activeProject.threat_profile_class || 'Vulnerable'}
                        </span>
                        <span className="text-[7px] text-text-muted font-bold font-mono tracking-widest uppercase mt-2">SVM CLASS</span>
                      </div>
                    </div>

                    {/* Score 5: Chain Fracture Probability (Logistic Regression) */}
                    <div className="glass-card p-6 bg-card border border-border-color flex items-center justify-between">
                      <div className="space-y-1.5 max-w-[55%]">
                        <span className="text-[9px] text-brand-warning font-extrabold uppercase tracking-widest block">
                          Shutdown Risk <span className="text-brand-warning text-[8px] tracking-wide block font-mono font-semibold">[Engine: Logistic Regression (Yes/No)]</span>
                        </span>
                        <h4 className="text-xl font-black text-text-main tracking-tight">Chain Fracture</h4>
                        <p className="text-[9px] text-text-muted leading-snug">Calculated likelihood that missing requirements trigger cascading halts.</p>
                      </div>

                      {/* SVG Gauge */}
                      <div className="relative w-24 h-24 flex items-center justify-center shrink-0 select-none">
                        <svg className="w-full h-full transform -rotate-90">
                          <circle cx="48" cy="48" r="40" stroke="var(--border-color)" strokeWidth="6" fill="transparent" />
                          <circle 
                            cx="48" cy="48" r="40" 
                            stroke="var(--brand-warning)" strokeWidth="6" fill="transparent" 
                            strokeDasharray={2 * Math.PI * 40}
                            strokeDashoffset={getStrokeDashoffset(activeProject.chain_fracture_probability || 45.0, 40)}
                            strokeLinecap="round"
                            className="transition-all duration-500 void-glow"
                          />
                        </svg>
                        <span className="absolute font-mono text-base font-black text-brand-warning">{Math.round(activeProject.chain_fracture_probability || 45.0)}%</span>
                      </div>
                    </div>

                    {/* Score 6: Liability Projection (Linear Regression) */}
                    <div className="glass-card p-6 bg-card border border-border-color flex items-center justify-between">
                      <div className="space-y-1.5 max-w-[55%]">
                        <span className="text-[9px] text-brand-success font-extrabold uppercase tracking-widest block">
                          Financial Liability <span className="text-brand-success text-[8px] tracking-wide block font-mono font-semibold">[Engine: Linear Regression (Numerical)]</span>
                        </span>
                        <h4 className="text-xl font-black text-text-main tracking-tight">Risk Projection</h4>
                        <p className="text-[9px] text-text-muted leading-snug">Estimated operational loss projection modeled against current omissions.</p>
                      </div>

                      {/* Value Display */}
                      <div className="relative w-24 h-24 flex flex-col items-center justify-center shrink-0 border border-border-color bg-bg rounded-xl select-none">
                        <span className="text-[14px] font-mono font-black text-brand-success tracking-tight">
                          ₹{Math.round(activeProject.financial_liability_projection || 500.0)}K
                        </span>
                        <span className="text-[7px] text-text-muted font-bold font-mono tracking-widest uppercase mt-2 text-center px-1">ESTIMATED LOSS</span>
                      </div>
                    </div>

                  </div>

                  {/* DYNAMIC SCENARIO SWITCHER PILLS & SANDBOX SLIDERS */}
                  {Array.isArray(activeProject.counterfactuals) && activeProject.counterfactuals.length > 0 && (
                    <div className="glass-card p-5 border border-brand-purple/20 bg-gradient-to-br from-card/30 to-transparent bg-card">
                      <h4 className="font-extrabold text-xs text-text-main tracking-widest uppercase mb-4 flex items-center justify-between border-b border-border-color/45 pb-3">
                        <span className="flex items-center space-x-2">
                          <Sliders className="w-4.5 h-4.5 text-brand-purple animate-pulse" />
                          <span>Dynamic Counterfactual Simulation Sandbox</span>
                        </span>
                        <span className="text-[8px] font-mono text-brand-purple font-bold tracking-wider">[Engine: Probability Shift Equations]</span>
                      </h4>
                      <p className="text-[11px] text-text-muted leading-normal mb-4">
                        Select a counterfactual preset pill to trigger alternative reality calculations, or customize individual parameters using the sliders below to recalculate the **Blindspot Index** in real-time.
                      </p>

                      {/* SCENARIO SWITCHER PILLS (NEW-GEN INTERACTION) */}
                      <div className="flex flex-wrap gap-2 mb-5">
                        <button
                          onClick={() => handleApplyScenario('normal')}
                          className={`px-3.5 py-1.5 rounded-lg border text-[9px] font-bold uppercase tracking-wider transition-all duration-200 cursor-pointer ${
                            activeScenario === 'normal' 
                              ? 'border-brand-primary bg-brand-primary/10 text-brand-primary font-black' 
                              : 'border-border-color bg-bg text-text-muted hover:border-border-color/85'
                          }`}
                        >
                          Normal Base (1.0x)
                        </button>
                        <button
                          onClick={() => handleApplyScenario('regulation')}
                          className={`px-3.5 py-1.5 rounded-lg border text-[9px] font-bold uppercase tracking-wider transition-all duration-200 cursor-pointer ${
                            activeScenario === 'regulation' 
                              ? 'border-brand-primary bg-brand-primary/10 text-brand-primary font-black' 
                              : 'border-border-color bg-bg text-text-muted hover:border-border-color/85'
                          }`}
                        >
                          Regulatory Tightening
                        </button>
                        <button
                          onClick={() => handleApplyScenario('drift')}
                          className={`px-3.5 py-1.5 rounded-lg border text-[9px] font-bold uppercase tracking-wider transition-all duration-200 cursor-pointer ${
                            activeScenario === 'drift' 
                              ? 'border-brand-primary bg-brand-primary/10 text-brand-primary font-black' 
                              : 'border-border-color bg-bg text-text-muted hover:border-border-color/85'
                          }`}
                        >
                          Traffic Concurrency Surge
                        </button>
                        <button
                          onClick={() => handleApplyScenario('cyberattack')}
                          className={`px-3.5 py-1.5 rounded-lg border text-[9px] font-bold uppercase tracking-wider transition-all duration-200 cursor-pointer ${
                            activeScenario === 'cyberattack' 
                              ? 'border-brand-primary bg-brand-primary/10 text-brand-primary font-black' 
                              : 'border-border-color bg-bg text-text-muted hover:border-border-color/85'
                          }`}
                        >
                          Zero-Day Cyberattack
                        </button>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {activeProject.counterfactuals.map((sc) => (
                          <div key={sc.id} className="bg-bg/60 p-4 border border-border-color rounded-lg space-y-2 text-xs">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-bold text-text-main tracking-wide truncate pr-2">{sc.name}</span>
                              <span className={`text-[9px] px-2 py-0.5 rounded font-mono font-extrabold tracking-wider ${
                                sc.status === 'Critical' ? 'bg-brand-danger/10 text-brand-danger border border-brand-danger/25' : 
                                sc.status === 'High' ? 'bg-brand-warning/10 text-brand-warning border border-brand-warning/25' : 'bg-brand-success/10 text-brand-success border border-brand-success/25'
                              }`}>
                                {sc.status}
                              </span>
                            </div>
                            <p className="text-[10px] text-text-muted leading-normal mb-3">{sc.description}</p>
                            
                            <div className="flex justify-between text-[10px] text-text-muted font-mono font-bold mb-1">
                              <span>Impact Coefficient: {sc.dynamic_impact || sc.base_impact}</span>
                              <span>Probability: {Math.round(sc.probability * 100)}%</span>
                            </div>

                            <input
                              type="range"
                              min="0.2"
                              max="2.0"
                              step="0.1"
                              value={sliderVals[sc.trigger_parameter] || 1.0}
                              onChange={(e) => {
                                handleSliderChange(sc.trigger_parameter, e.target.value);
                                setActiveScenario('custom'); // flag custom preset override
                              }}
                              className="w-full h-1 bg-border-color rounded-lg appearance-none cursor-pointer accent-brand-purple transition-all"
                            />
                            <div className="flex justify-between text-[8px] text-text-muted font-bold font-mono tracking-wider">
                              <span>0.2x (Minimal Shock)</span>
                              <span>1.0x (Standard)</span>
                              <span>2.0x (Extreme Shock)</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* DISCOVERY SHEET (NEW-GEN UNKNOWN UNKNOWN UI - COLLAPSIBLE GAPS) */}
                  <div className="glass-card p-5 bg-card border border-border-color">
                    <h4 className="font-extrabold text-xs text-text-main tracking-widest uppercase mb-4 flex items-center justify-between border-b border-border-color pb-3">
                      <span className="flex items-center space-x-2">
                        <ShieldAlert className="w-4.5 h-4.5 text-brand-primary" />
                        <span>Discovery Sheet (Missing Requirements Ledger)</span>
                      </span>
                      <span className="text-[8px] font-mono text-brand-primary font-bold tracking-wider">[Engine: Neo4j Cypher Diff]</span>
                    </h4>
                    
                    {activeProject.missing_factors.length === 0 ? (
                      <div className="text-xs text-brand-success py-2 font-semibold">
                        ✓ Clean Audit: All domain expectation nodes are perfectly accounted for in your specifications!
                      </div>
                    ) : (
                      <div className="space-y-2.5">
                        {activeProject.missing_factors.map((gap, i) => {
                          const isExpanded = expandedGap === i;
                          return (
                            <div 
                              key={i} 
                              className="border border-border-color bg-bg/50 p-4 rounded-xl transition-all duration-200 text-xs"
                            >
                              <div 
                                onClick={() => setExpandedGap(isExpanded ? null : i)}
                                className="flex items-center justify-between cursor-pointer select-none"
                              >
                                <div className="flex items-center space-x-2.5">
                                  <span className="text-brand-danger font-mono">●</span>
                                  <span className="font-bold text-text-main uppercase tracking-wide">{gap.requirement}</span>
                                  <span className="text-[9px] bg-brand-primary/10 border border-brand-primary/25 px-2 py-0.5 rounded-full text-brand-primary font-extrabold uppercase">
                                    {gap.category}
                                  </span>
                                  {gap.fractured_chain && (
                                    <span className="text-[8px] bg-brand-danger/10 text-brand-danger px-1.5 py-0.5 border border-brand-danger/25 rounded font-mono uppercase font-bold tracking-wider">
                                      Chain Fractured
                                    </span>
                                  )}
                                </div>
                                <span className="text-[10px] text-text-muted hover:text-text-main transition-colors flex items-center space-x-1 font-bold uppercase tracking-wider font-sans">
                                  <span>{isExpanded ? 'Hide Details' : 'View Reasoning'}</span>
                                  <span>→</span>
                                </span>
                              </div>
                              
                              {isExpanded && (
                                <div className="mt-3 pt-3 border-t border-border-color/60 space-y-3 leading-relaxed text-justify animate-fade-in">
                                  <p className="text-text-muted font-medium">{gap.description}</p>
                                  <div className="bg-brand-danger/5 border border-brand-danger/25 p-3 rounded-lg text-brand-danger leading-snug">
                                    <strong className="font-bold uppercase text-[9px] tracking-wider block mb-0.5">Downstream Cascading Hazard:</strong>
                                    "{gap.risk}"
                                  </div>
                                </div>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>



                  {/* SILENT ASSUMPTIONS STRESS TEST MATRIX */}
                  <div className="glass-card p-5 bg-card border border-border-color">
                    <h4 className="font-extrabold text-xs text-text-main tracking-widest uppercase mb-4 flex items-center justify-between border-b border-border-color pb-3">
                      <span className="flex items-center space-x-2">
                        <AlertTriangle className="w-4.5 h-4.5 text-brand-warning" />
                        <span>Silent Assumption Stress Test Matrix</span>
                      </span>
                      <span className="text-[8px] font-mono text-brand-warning font-bold tracking-wider">[Engine: Parser Regex]</span>
                    </h4>

                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-xs leading-normal font-sans">
                        <thead>
                          <tr className="border-b border-border-color text-text-muted text-[10px] uppercase tracking-wider font-bold">
                            <th className="py-2.5 pr-4">Identified Implicit Assertion</th>
                            <th className="py-2.5 px-4 w-28 text-center">Fragility Index</th>
                            <th className="py-2.5 pl-4">Targeted Adversarial stress question</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-border-color/40 text-text-muted">
                          {activeProject.assumptions.map((ass, i) => (
                            <tr key={i} className="hover:bg-bg/25 transition-colors">
                              <td className="py-3 pr-4 text-justify pr-6">
                                <span className="text-text-main font-medium block">"{ass.claim}"</span>
                                <span className="text-[9px] text-brand-warning font-semibold italic mt-1.5 inline-block">
                                  Vulnerability: {ass.vulnerability}
                                </span>
                              </td>
                              <td className="py-3 px-4 text-center">
                                <span className={`px-2 py-0.5 rounded-full font-mono font-bold text-[11px] inline-block ${
                                  ass.fragility_score >= 8 ? 'bg-brand-danger/10 text-brand-danger' : 
                                  ass.fragility_score >= 5 ? 'bg-brand-warning/10 text-brand-warning' : 'bg-brand-success/10 text-brand-success'
                                }`}>
                                  {ass.fragility_score}/10
                                </span>
                              </td>
                              <td className="py-3 pl-4 text-brand-primary text-justify italic leading-relaxed">
                                "{ass.attack_question}"
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* CONSEQUENCE FLOW GRAPH (React Flow) */}
                  <div className="glass-card p-5 bg-card border border-border-color">
                    <h4 className="font-extrabold text-xs text-text-main tracking-widest uppercase mb-4 flex items-center justify-between border-b border-border-color pb-3">
                      <span className="flex items-center space-x-2">
                        <Layers className="w-4.5 h-4.5 text-brand-primary" />
                        <span>Active Consequence Ripple Trees Viewer</span>
                      </span>
                      <span className="text-[8px] font-mono text-brand-primary font-bold tracking-wider">[Engine: Causal Path Propagation]</span>
                    </h4>
                    <p className="text-[11px] text-text-muted leading-normal mb-4">
                      Interactive node map tracing downstream failure propagation when architectural design gaps trigger operational shocks. Use the controls to fit view, zoom, and explore connections.
                    </p>
                    <FlowViewer treeData={activeProject.consequence_tree} />
                  </div>
                  {/* TABBED INTERFACES FOR FAILURE DNA AND ADVERSARIAL BOARD */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    
                    {/* Left Side: Failure DNA Map */}
                    <div className="glass-card p-6 h-fit bg-card border border-border-color">
                      <h3 className="font-extrabold text-sm text-text-main tracking-widest uppercase mb-5 flex items-center justify-between border-b border-border-color pb-3">
                        <span className="flex items-center space-x-2">
                          <BarChart2 className="w-4.5 h-4.5 text-brand-danger" />
                          <span>Disaster DNA Map</span>
                        </span>
                        <span className="text-[8px] font-mono text-brand-danger font-bold tracking-wider">[Engine: Cosine Semantic Match]</span>
                      </h3>
                      <FailureDNAMap failureDna={activeProject.failure_dna} />
                    </div>

                    {/* Right Side: Adversarial debate panel */}
                    <div className="glass-card p-6 h-fit bg-card border border-border-color">
                      <h3 className="font-extrabold text-sm text-text-main tracking-widest uppercase mb-5 flex items-center justify-between border-b border-border-color pb-3">
                        <span className="flex items-center space-x-2">
                          <MessageSquare className="w-4.5 h-4.5 text-brand-purple" />
                          <span>Boardroom Clash Feed</span>
                        </span>
                        <span className="text-[8px] font-mono text-brand-purple font-bold tracking-wider">[Engine: Room Persona Generators]</span>
                      </h3>
                      <ExpertDebate 
                        expertReviews={activeProject.expert_reviews} 
                        boardDisagreements={activeProject.board_disagreements} 
                      />
                    </div>

                  </div>

                </div>
              )}
            </div>
          )}

          {/* ==================================================== */}
          {/* TAB 3: NEO4J EXPECTATION GRAPH EXPLORER */}
          {/* ==================================================== */}
          {activeTab === 'expectation_graph' && (
            <div className="glass-card p-6 animate-fade-in space-y-5 bg-card border border-border-color">
              <div className="flex items-center justify-between border-b border-border-color pb-3">
                <h3 className="font-extrabold text-sm text-text-main tracking-widest uppercase flex items-center space-x-2">
                  <Network className="w-4.5 h-4.5 text-brand-purple" />
                  <span>Neo4j Graph Expectation Network</span>
                </h3>
                <span className="text-[9px] font-mono text-brand-cyan bg-brand-cyan/10 px-2 py-0.5 border border-brand-cyan/20 rounded uppercase font-bold tracking-widest">
                  [Engine: Neo4j Schema Cypher]
                </span>
              </div>
              
              <p className="text-[11px] text-text-muted leading-relaxed">
                This graph compiles the baseline target requirements for the active domain **{activeProject?.domain || 'Healthcare'}** loaded directly from your cloud-hosted **Neo4j Aura database**. Nodes colored in green are successfully addressed; nodes colored in red represent absolute voids in your specification.
              </p>

              {activeProject ? (
                <FlowViewer treeData={getExpectationGraphData()} />
              ) : (
                <div className="flex flex-col items-center justify-center h-80 bg-bg border border-border-color rounded-xl">
                  <span className="text-text-muted text-xs">Select or analyze a project to query its expectation network.</span>
                </div>
              )}
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
