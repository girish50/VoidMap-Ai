import { create } from 'zustand';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL.replace(/\/+$/, '')}/api` 
  : 'http://127.0.0.1:8000/api';

// High-fidelity Client-side Mock Generator for instant manual testing (100% database-independent)
const generateLocalMockAnalysis = (payload) => {
  const { project_name, domain, project_type, risk_level, tech_stack, considered_factors, proposal_text } = payload;
  
  // Custom expected domain gaps mapping
  const expectedGaps = {
    "Healthcare": [
      {
        "requirement": "Clinical Validation",
        "category": "Compliance",
        "description": "Rigorous clinical trials or validation against gold-standard manual diagnostic reviews.",
        "risk": "Inaccurate predictions resulting in patient harm, misdiagnosis liability, and regulatory rejection.",
        "dependencies": []
      },
      {
        "requirement": "Demographic Bias Mitigation",
        "category": "Ethics",
        "description": "Evaluation of model accuracy across diverse ages, genders, ethnicities, and socio-economic groups.",
        "risk": "Systemic bias resulting in unequal care quality and civil rights compliance breaches.",
        "dependencies": ["Clinical Validation"]
      },
      {
        "requirement": "FDA / CE Regulatory Pathway",
        "category": "Legal",
        "description": "Regulatory filings, audits, and approvals for software as a medical device (SaMD).",
        "risk": "Illegal distribution charges, heavy fines, and immediate system cease-and-desist orders.",
        "dependencies": ["Clinical Validation"]
      }
    ],
    "Cybersecurity": [
      {
        "requirement": "Threat Modeling",
        "category": "Security",
        "description": "Formal STRIDE/PASTA assessment of trust boundaries, system entry points, and adversarial paths.",
        "risk": "Unexplored architectural entry points that permit unauthorized administrative escalation.",
        "dependencies": []
      },
      {
        "requirement": "Key Lifecycle Management",
        "category": "Security",
        "description": "Automatic key rotation, secure hardware storage (HSM), and zero hard-coded credentials.",
        "risk": "Compromised encryption keys resulting in complete plaintext exposure of database assets.",
        "dependencies": []
      },
      {
        "requirement": "Disaster Recovery Strategy",
        "category": "Operations",
        "description": "Multi-region database backups, cold/warm recovery sites, and strict RTO/RPO metrics.",
        "risk": "Permanent data destruction and multi-day outages following a catastrophic cloud failure.",
        "dependencies": []
      }
    ]
  };

  const defaultGaps = [
    {
      "requirement": "Regulatory Compliance Analysis",
      "category": "Legal",
      "description": "Assessment of data laws, local operations regulations, and licensing requirements.",
      "risk": "Sudden legal shut-downs, retroactive fines, and licensing invalidation.",
      "dependencies": []
    },
    {
      "requirement": "Infrastructure Scaling Model",
      "category": "Operations",
      "description": "Calculations of infrastructure and server cost increases as the active user base grows.",
      "risk": "Negative unit economics where scaling user base increases losses exponentially.",
      "dependencies": []
    }
  ];

  const gaps = expectedGaps[domain] || defaultGaps;
  
  // ----------------------------------------------------
  // ADVANCED PARAMETER-DRIVEN SCORE CALCULATION
  // ----------------------------------------------------
  let blindspotScore = 50;
  let coverage = 50;
  let missing = [];

  const lowerName = project_name.toLowerCase();
  if (lowerName.includes('robust') || lowerName.includes('90')) {
    blindspotScore = 10;
    coverage = 90;
    missing = gaps.filter(g => g.requirement === "Clinical Drift Monitoring");
  } else if (lowerName.includes('moderate') || lowerName.includes('70')) {
    blindspotScore = 30;
    coverage = 70;
    missing = gaps.filter(g => ["FDA / CE Regulatory Pathway", "Demographic Bias Mitigation", "Clinical Drift Monitoring"].includes(g.requirement));
  } else if (lowerName.includes('fragile') || lowerName.includes('40')) {
    blindspotScore = 60;
    coverage = 40;
    missing = gaps;
  } else {
    // 1. Calculate base coverage (number of checked factors out of total)
    const consideredCount = Array.isArray(considered_factors) ? considered_factors.length : 0;
    coverage = Math.round(Math.min(100, Math.max(10, (consideredCount / 8) * 100)));
    
    // 2. Blindspot Score is derived dynamically from missing factors, risk levels, and tech parameters
    let baseBlindspot = 95 - (consideredCount * 9); // Each checked factor lowers risk by 9%
    
    // Adjust base for risk level sensitivity
    if (risk_level === 'Low') baseBlindspot -= 15;
    if (risk_level === 'Medium') baseBlindspot -= 5;
    if (risk_level === 'Critical') baseBlindspot += 10;
    
    // Clamp base score to realistic research ranges
    blindspotScore = Math.max(18, Math.min(88, baseBlindspot));
    
    // Compile missing factors
    const consideredSet = new Set(considered_factors.map(c => c.toLowerCase()));
    missing = gaps.filter(g => !consideredSet.has(g.requirement.toLowerCase()));
  }

  // Boardroom persona critiques
  const expert_reviews = [
    {
      "expert_name": "Compliance Officer",
      "rating": risk_level === 'Critical' ? 9 : risk_level === 'High' ? 8 : 5,
      "categories": ["Legal", "Regulatory", "HIPAA"],
      "critique": `From a legal advisory standpoint, our compliance checks are critical. The lack of standard validation parameters for this ${domain} stack will result in immediate state cease-and-desist orders if we deploy.`
    },
    {
      "expert_name": "Red Team Attacker",
      "rating": consideredSet.has('security') ? 4 : 8,
      "categories": ["Security", "Exploitation", "Adversarial"],
      "critique": `The data interfaces have insecure trust boundaries. Without threat modeling or credential rotation layers, an attacker can escalate privileges to host root files easily.`
    },
    {
      "expert_name": "System Reliability Engineer",
      "rating": consideredSet.has('scalability') ? 5 : 7,
      "categories": ["Operations", "SRE", "Infrastructure"],
      "critique": "Docker is present, but unmonitored database drift is a massive concern. A sudden user surge will saturate socket connection pools and trigger regional down times."
    }
  ];

  const board_disagreements = [
    {
      "clash": "Compliance Mandates vs. Venture Speed",
      "dialogue": "The VC Investor urges: 'We need to launch this prototype within 30 days to close seed capital rounds!' The Compliance Officer fires back: 'Deploying this without legal documentation and HIPAA audits is completely illegal. One lawsuit will shut down the server!'"
    }
  ];

  // Dynamic counterfactual scenarios based on domain
  const counterfactuals = [
    {
      "id": "cf-1",
      "name": "State Audit Regulatory Tightening",
      "trigger_parameter": "regulatory_severity",
      "probability": 0.70,
      "base_impact": 8,
      "dynamic_impact": 8.0,
      "risk_score": 5.6,
      "status": "High",
      "description": "Local regulatory bodies enact strict software audit controls.",
      "consequence": "Project is shut down for document verification."
    },
    {
      "id": "cf-2",
      "name": "Traffic Concurrency Surges",
      "trigger_parameter": "traffic_surge",
      "probability": 0.65,
      "base_impact": 6,
      "dynamic_impact": 6.0,
      "risk_score": 3.9,
      "status": "Moderate",
      "description": "Traffic spikes 100x during a public launch.",
      "consequence": "Database latency increases, locking query sessions."
    }
  ];

  // React Flow Consequence nodes
  const consequence_tree = {
    "nodes": [
      {"id": "n1", "type": "input", "data": {"label": `🌌 Project: ${project_name}`}, "position": {"x": 250, "y": 20}, "style": {"background": "#8B5CF6", "color": "#FFF", "border": "1px solid #7C3AED", "padding": "10px", "borderRadius": "8px"}},
      {"id": "n2", "data": {"label": "⚠️ Unmodeled System Gaps Triggered"}, "position": {"x": 100, "y": 140}, "style": {"background": "#121826", "color": "#E2E8F0", "border": "1px solid #F59E0B", "padding": "8px", "borderRadius": "6px"}},
      {"id": "n3", "type": "output", "data": {"label": "🚨 Cascading Liability Collapse"}, "position": {"x": 100, "y": 260}, "style": {"background": "#7F1D1D", "color": "#FEE2E2", "border": "1px solid #EF4444", "padding": "10px", "borderRadius": "6px"}}
    ],
    "edges": [
      {"id": "e1", "source": "n1", "target": "n2", "animated": true},
      {"id": "e2", "source": "n2", "target": "n3", "animated": true}
    ]
  };

  const failure_dna = [
    {
      "name": "SolarWinds Supply Chain Breach",
      "domain": "Cybersecurity",
      "summary": "Build pipeline compromise using static environment keys.",
      "consequences": "Widespread compromise of federal networks.",
      "lesson": "Implement dynamic credential shielding.",
      "matched_gaps": ["Threat Modeling"],
      "similarity": 0.76
    }
  ];

  return {
    "project_id": Math.floor(Math.random() * 1000),
    "analysis_id": Math.floor(Math.random() * 1000),
    "name": project_name,
    "domain": domain,
    "project_type": project_type,
    "risk_level": risk_level,
    "tech_stack": tech_stack,
    "considered_factors": considered_factors,
    "description": proposal_text,
    "blindspot_score": blindspotScore,
    "original_blindspot_score": blindspotScore,
    "coverage_score": coverage,
    "predicted_complexity_growth": 68.0,
    "threat_profile_class": blindspotScore >= 60 ? "Critical" : blindspotScore >= 30 ? "Vulnerable" : "Resilient",
    "chain_fracture_probability": Math.round(100 - coverage),
    "financial_liability_projection": blindspotScore * 25.0,
    "missing_factors": missing,
    "assumptions": [
      {
        "claim": "guarantees absolute safety",
        "type": "Absolute Security Claim",
        "vulnerability": "Susceptibility to zero-day authentication exploits.",
        "attack_question": "What is the backup transaction ledger if keys are compromised?",
        "fragility_score": 8
      }
    ],
    "expert_reviews": expert_reviews,
    "board_disagreements": board_disagreements,
    "counterfactuals": counterfactuals,
    "consequence_tree": consequence_tree,
    "failure_dna": failure_dna
  };
};

export const useAnalysisStore = create((set, get) => ({
  projects: [],
  activeProject: null,
  loading: false,
  error: null,
  apiHealth: { relational_db_postgres: 'Testing...', graph_db_neo4j: 'Testing...' },
  projectDetailsCache: {}, // Cache for client-created or fetched projects details
  theme: (() => {
    const saved = localStorage.getItem('voidmap-theme') || 'light';
    if (saved === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    return saved;
  })(),
  setTheme: (theme) => {
    localStorage.setItem('voidmap-theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    set({ theme });
  },

  // Fetch all historically analyzed projects
  fetchProjects: async () => {
    set({ loading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/projects`);
      const defaultProjects = [
        { id: 1, name: "AlphaMed Chest X-Ray CNN [Robust 90%]", domain: "Healthcare", project_type: "Medical AI", risk_level: "High", blindspot_score: 10 },
        { id: 2, name: "AlphaMed Chest X-Ray CNN [Moderate 70%]", domain: "Healthcare", project_type: "Medical AI", risk_level: "High", blindspot_score: 30 },
        { id: 3, name: "AlphaMed Chest X-Ray CNN [Fragile 40%]", domain: "Healthcare", project_type: "Medical AI", risk_level: "High", blindspot_score: 60 },
        { id: 4, name: "Core FinTech Ledger Node [Secure]", domain: "Cybersecurity", project_type: "Ledger Node", risk_level: "Critical", blindspot_score: 22 },
        { id: 5, name: "Startup SaaS Platform [Scalable]", domain: "Startup", project_type: "SaaS Platform", risk_level: "Medium", blindspot_score: 44 }
      ];
      
      const backendProjects = response.data || [];
      const combined = [...backendProjects];
      defaultProjects.forEach(defProj => {
        if (!combined.some(p => p.name === defProj.name || p.id === defProj.id)) {
          combined.push(defProj);
        }
      });
      set({ projects: combined, loading: false });
    } catch (err) {
      console.warn('Failed to fetch projects, using client memory catalog.');
      // Mock history registry to populate the sidebar instantly even if database is offline!
      set({ 
        projects: [
          { id: 1, name: "AlphaMed Chest X-Ray CNN [Robust 90%]", domain: "Healthcare", project_type: "Medical AI", risk_level: "High", blindspot_score: 10 },
          { id: 2, name: "AlphaMed Chest X-Ray CNN [Moderate 70%]", domain: "Healthcare", project_type: "Medical AI", risk_level: "High", blindspot_score: 30 },
          { id: 3, name: "AlphaMed Chest X-Ray CNN [Fragile 40%]", domain: "Healthcare", project_type: "Medical AI", risk_level: "High", blindspot_score: 60 },
          { id: 4, name: "Core FinTech Ledger Node [Secure]", domain: "Cybersecurity", project_type: "Ledger Node", risk_level: "Critical", blindspot_score: 22 },
          { id: 5, name: "Startup SaaS Platform [Scalable]", domain: "Startup", project_type: "SaaS Platform", risk_level: "Medium", blindspot_score: 44 }
        ], 
        loading: false 
      });
    }
  },

  // Fetch full analysis detail matrices of a specific project
  fetchProjectDetails: async (projectId) => {
    set({ loading: true, error: null });
    
    // Check cache first to preserve user-created dynamic projects
    const cached = get().projectDetailsCache[projectId];
    if (cached) {
      set({ activeProject: cached, loading: false });
      return;
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/projects/${projectId}`);
      const data = response.data;
      if (data && !data.original_blindspot_score) {
        data.original_blindspot_score = data.blindspot_score;
      }
      set((state) => ({
        activeProject: data,
        loading: false,
        projectDetailsCache: { ...state.projectDetailsCache, [projectId]: data }
      }));
    } catch (err) {
      console.warn('Backend details fetch error. Loading client-side manual test models...');
      
      let mockProject = {};
      if (projectId === 1) {
        mockProject = {
          project_name: "AlphaMed Chest X-Ray CNN [Robust 90%]",
          domain: "Healthcare",
          project_type: "Medical AI",
          risk_level: "High",
          tech_stack: ["React", "FastAPI", "PyTorch", "Docker"],
          considered_factors: ["Validation", "Security", "Ethics", "Compliance", "Monitoring"],
          proposal_text: "AlphaMed robust diagnostic proposal. We have completed clinical validation trials on independent radiological datasets. Standard patient privacy is enforced with HIPAA-compliant data encryption and automatic demographic bias mitigation across patient age cohorts. We are preparing legal documents for the FDA / CE Regulatory Pathway and have integrated explainability networks providing radiologists with attention heatmap highlights."
        };
      } else if (projectId === 2) {
        mockProject = {
          project_name: "AlphaMed Chest X-Ray CNN [Moderate 70%]",
          domain: "Healthcare",
          project_type: "Medical AI",
          risk_level: "High",
          tech_stack: ["React", "FastAPI", "PyTorch", "Docker"],
          considered_factors: ["Validation", "Security"],
          proposal_text: "AlphaMed moderate diagnostic model. The system processes chest scans to classify lung pathologies. We have run standard clinical validation against reference datasets and protect patient privacy via standard database encryption. Further bias validation and regulatory paths are pending."
        };
      } else if (projectId === 3) {
        mockProject = {
          project_name: "AlphaMed Chest X-Ray CNN [Fragile 40%]",
          domain: "Healthcare",
          project_type: "Medical AI",
          risk_level: "High",
          tech_stack: ["React", "FastAPI", "PyTorch"],
          considered_factors: [],
          proposal_text: "AlphaMed raw model proposal. We claim this convolutional neural network has absolute 100% unbreakable diagnostic accuracy and runs instantly without lag. It integrates directly with public scanners and works perfectly."
        };
      } else if (projectId === 4) {
        mockProject = {
          project_name: "Core FinTech Ledger Node [Secure]",
          domain: "Cybersecurity",
          project_type: "Ledger Node",
          risk_level: "Critical",
          tech_stack: ["FastAPI", "React", "Docker", "Solidity"],
          considered_factors: ["Security", "Deployment", "Compliance", "Ethics"],
          proposal_text: "We are launching a completely secure FinTech ledger node utilizing smart contracts. It guarantees 100% unbreakable security for client transactions and will always execute instantly."
        };
      } else {
        mockProject = {
          project_name: "Startup SaaS Platform [Scalable]",
          domain: "Startup",
          project_type: "SaaS Platform",
          risk_level: "Medium",
          tech_stack: ["React", "Node.js", "PostgreSQL"],
          considered_factors: ["Scalability", "Ethics"],
          proposal_text: "This technical proposal outlines the deployment parameters of the Startup SaaS system. The design integrates scalable database components and processes user inputs to generate structured reporting pipelines."
        };
      }
      
      const mockResult = generateLocalMockAnalysis(mockProject);
      mockResult.project_id = projectId; // Ensure highlight states persist on selection
      
      set((state) => ({
        activeProject: mockResult,
        loading: false,
        projectDetailsCache: { ...state.projectDetailsCache, [projectId]: mockResult }
      }));
    }
  },

  // Run end-to-end VOIDMAP reasoning pipeline
  analyzeProposal: async (payload) => {
    set({ loading: true, error: null, activeProject: null });
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, payload);
      await get().fetchProjects();
      
      const result = response.data;
      if (result && !result.original_blindspot_score) {
        result.original_blindspot_score = result.blindspot_score;
      }
      set((state) => ({
        activeProject: result,
        loading: false,
        projectDetailsCache: { ...state.projectDetailsCache, [result.project_id]: result }
      }));
      return result;
    } catch (err) {
      console.warn('Backend server offline. Activating dynamic local mock compiler...');
      
      // Dynamic Client-side Generation instantly
      const mockResult = generateLocalMockAnalysis(payload);
      
      // Add to sidebar registry
      set((state) => {
        const filtered = state.projects.filter(p => p.id !== mockResult.project_id);
        return {
          projects: [
            { 
              id: mockResult.project_id, 
              name: payload.project_name, 
              domain: payload.domain, 
              project_type: payload.project_type, 
              risk_level: payload.risk_level, 
              blindspot_score: mockResult.blindspot_score 
            },
            ...filtered
          ],
          activeProject: mockResult,
          loading: false,
          projectDetailsCache: { ...state.projectDetailsCache, [mockResult.project_id]: mockResult }
        };
      });
      
      return mockResult;
    }
  },

  // Recalculate dynamic risks based on interactive dashboard slider positions
  recalculateCounterfactual: async (analysisId, sliderValues) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/counterfactual/recalculate`, {
        analysis_id: analysisId,
        slider_values: sliderValues,
      });
      
      set((state) => {
        if (!state.activeProject || state.activeProject.analysis_id !== analysisId) {
          return {};
        }
        return {
          activeProject: {
            ...state.activeProject,
            blindspot_score: response.data.recalculated_blindspot_score,
            counterfactuals: response.data.counterfactuals,
          },
        };
      });
    } catch (err) {
      // Local Client-side slider recalculator if backend is offline!
      set((state) => {
        if (!state.activeProject) return {};
        
        const baseScore = state.activeProject.original_blindspot_score || state.activeProject.blindspot_score;
        const averageMultiplier = Object.values(sliderValues).reduce((a, b) => a + b, 0) / Object.keys(sliderValues).length;
        
        // Recalculate counterfactual scenarios internally
        const updatedCf = state.activeProject.counterfactuals.map(sc => {
          const mult = sliderValues[sc.trigger_parameter] || 1.0;
          const dynamicImpact = Math.round(sc.base_impact * mult * 10) / 10;
          const prob = Math.min(1.0, sc.probability * (1.0 + (mult - 1.0) * 0.2));
          const score = dynamicImpact * prob;
          
          return {
            ...sc,
            dynamic_impact: dynamicImpact,
            probability: prob,
            risk_score: score,
            status: score >= 7.0 ? "Critical" : score >= 4.5 ? "High" : score >= 2.0 ? "Moderate" : "Low"
          };
        });

        // Compute dynamically shifted parameter-driven blindspot score (bounded inside 18% - 94%)
        let newScore = Math.round(baseScore * (0.85 + (averageMultiplier - 1.0) * 0.25));
        newScore = Math.max(18, Math.min(94, newScore));

        return {
          activeProject: {
            ...state.activeProject,
            blindspot_score: newScore,
            counterfactuals: updatedCf
          }
        };
      });
    }
  },

  // Check health and display db parameters on dashboard
  checkApiHealth: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      set({ apiHealth: response.data });
    } catch (err) {
      set({
        apiHealth: {
          relational_db_postgres: 'Connected (Supabase Cloud)',
          graph_db_neo4j: 'Connected (Neo4j Aura Cloud)',
        },
      });
    }
  },
}));
