import logging
from typing import List, Dict, Any

logger = logging.getLogger("voidmap.engine.consequence")
logging.basicConfig(level=logging.INFO)

class ConsequenceTreeGenerator:
    """
    VOIDMAP Consequence & Downstream Ripple Engine.
    Generates a structured multi-level flow tree of consequences, fully mapped for React Flow rendering.
    """
    @staticmethod
    def generate_tree(
        project_name: str, 
        domain: str, 
        missing_requirements: List[str]
    ) -> Dict[str, Any]:
        """
        Creates primary, secondary, and tertiary downstream ripple effects.
        Maps them as nodes and edges with calculated 2D positions for visual layout.
        """
        logger.info("Generating dynamic Consequence Tree...")
        
        missing_set = set(missing_requirements)
        
        # Base Node List
        nodes = []
        edges = []
        
        # 1. Level 0 Node (Root)
        nodes.append({
            "id": "root",
            "type": "input",
            "data": {"label": f"🌌 Project: {project_name}"},
            "position": {"x": 250, "y": 20},
            "style": {"background": "#6366F1", "color": "#FFFFFF", "border": "1px solid #4F46E5", "padding": "10px", "borderRadius": "8px"}
        })
        
        # Determine Domain Ripples
        if domain == "Healthcare":
            # Primary Nodes
            nodes.extend([
                {
                    "id": "hc-p1",
                    "data": {"label": "Deploy CNN Classifier to Hospital Cloud"},
                    "position": {"x": 80, "y": 140},
                    "style": {"background": "#1E293D", "color": "#E2E8F0", "border": "1px solid #10B981", "padding": "8px", "borderRadius": "6px"}
                },
                {
                    "id": "hc-p2",
                    "data": {"label": "Process Patient X-Ray Scans"},
                    "position": {"x": 420, "y": 140},
                    "style": {"background": "#1E293D", "color": "#E2E8F0", "border": "1px solid #10B981", "padding": "8px", "borderRadius": "6px"}
                }
            ])
            edges.extend([
                {"id": "e-root-p1", "source": "root", "target": "hc-p1", "animated": True},
                {"id": "e-root-p2", "source": "root", "target": "hc-p2", "animated": True}
            ])
            
            # Secondary Gaps
            if "Clinical Drift Monitoring" in missing_set:
                nodes.append({
                    "id": "hc-s1",
                    "data": {"label": "⚠️ Unmonitored Scanner Hardware Noise"},
                    "position": {"x": 80, "y": 260},
                    "style": {"background": "#3B1824", "color": "#FDA4AF", "border": "1px solid #F43F5E", "padding": "8px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-p1-s1", "source": "hc-p1", "target": "hc-s1", "animated": True})
                
                # Tertiary Outcome
                nodes.append({
                    "id": "hc-t1",
                    "type": "output",
                    "data": {"label": "🚨 Silent Misdiagnoses & Malpractice Lawsuits"},
                    "position": {"x": 80, "y": 380},
                    "style": {"background": "#7F1D1D", "color": "#FEE2E2", "border": "1px solid #EF4444", "padding": "10px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-s1-t1", "source": "hc-s1", "target": "hc-t1", "animated": True})
            else:
                nodes.append({
                    "id": "hc-s1",
                    "data": {"label": "Scan Calibration Alerts Triggered"},
                    "position": {"x": 80, "y": 260},
                    "style": {"background": "#121826", "color": "#E2E8F0", "border": "1px solid #1F293D", "padding": "8px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-p1-s1", "source": "hc-p1", "target": "hc-s1"})
                
            if "FDA / CE Regulatory Pathway" in missing_set:
                nodes.append({
                    "id": "hc-s2",
                    "data": {"label": "⚠️ Unlicensed Medical Device Filing Audit"},
                    "position": {"x": 420, "y": 260},
                    "style": {"background": "#3B1824", "color": "#FDA4AF", "border": "1px solid #F43F5E", "padding": "8px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-p2-s2", "source": "hc-p2", "target": "hc-s2", "animated": True})
                
                nodes.append({
                    "id": "hc-t2",
                    "type": "output",
                    "data": {"label": "🚨 Federal Cease-and-Desist & Multi-Million Fines"},
                    "position": {"x": 420, "y": 380},
                    "style": {"background": "#7F1D1D", "color": "#FEE2E2", "border": "1px solid #EF4444", "padding": "10px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-s2-t2", "source": "hc-s2", "target": "hc-t2", "animated": True})
            else:
                nodes.append({
                    "id": "hc-s2",
                    "data": {"label": "Standard FDA Regulatory Dossiers Generated"},
                    "position": {"x": 420, "y": 260},
                    "style": {"background": "#121826", "color": "#E2E8F0", "border": "1px solid #1F293D", "padding": "8px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-p2-s2", "source": "hc-p2", "target": "hc-s2"})

        elif domain == "Cybersecurity":
            nodes.extend([
                {
                    "id": "sec-p1",
                    "data": {"label": "Initiate Build Pipelines"},
                    "position": {"x": 80, "y": 140},
                    "style": {"background": "#1E293D", "color": "#E2E8F0", "border": "1px solid #10B981", "padding": "8px", "borderRadius": "6px"}
                },
                {
                    "id": "sec-p2",
                    "data": {"label": "Expose Administrative Panel APIs"},
                    "position": {"x": 420, "y": 140},
                    "style": {"background": "#1E293D", "color": "#E2E8F0", "border": "1px solid #10B981", "padding": "8px", "borderRadius": "6px"}
                }
            ])
            edges.extend([
                {"id": "e-root-p1", "source": "root", "target": "sec-p1", "animated": True},
                {"id": "e-root-p2", "source": "root", "target": "sec-p2", "animated": True}
            ])
            
            if "Threat Modeling" in missing_set:
                nodes.append({
                    "id": "sec-s1",
                    "data": {"label": "⚠️ Unaudited System Trust Boundaries"},
                    "position": {"x": 80, "y": 260},
                    "style": {"background": "#3B1824", "color": "#FDA4AF", "border": "1px solid #F43F5E", "padding": "8px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-p1-s1", "source": "sec-p1", "target": "sec-s1", "animated": True})
                
                nodes.append({
                    "id": "sec-t1",
                    "type": "output",
                    "data": {"label": "🚨 Malicious Code Injected in Build Packages"},
                    "position": {"x": 80, "y": 380},
                    "style": {"background": "#7F1D1D", "color": "#FEE2E2", "border": "1px solid #EF4444", "padding": "10px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-s1-t1", "source": "sec-s1", "target": "sec-t1", "animated": True})
                
            if "Key Lifecycle Management" in missing_set:
                nodes.append({
                    "id": "sec-s2",
                    "data": {"label": "⚠️ Hardcoded Admin Keys in Config Repo"},
                    "position": {"x": 420, "y": 260},
                    "style": {"background": "#3B1824", "color": "#FDA4AF", "border": "1px solid #F43F5E", "padding": "8px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-p2-s2", "source": "sec-p2", "target": "sec-s2", "animated": True})
                
                nodes.append({
                    "id": "sec-t2",
                    "type": "output",
                    "data": {"label": "🚨 SQL Injection Escalation & Database Ransomware"},
                    "position": {"x": 420, "y": 380},
                    "style": {"background": "#7F1D1D", "color": "#FEE2E2", "border": "1px solid #EF4444", "padding": "10px", "borderRadius": "6px"}
                })
                edges.append({"id": "e-s2-t2", "source": "sec-s2", "target": "sec-t2", "animated": True})

        # Generic Domain Consequence Tree
        else:
            nodes.extend([
                {
                    "id": "gen-p1",
                    "data": {"label": "Launch Initial Prototype Product"},
                    "position": {"x": 80, "y": 140},
                    "style": {"background": "#1E293D", "color": "#E2E8F0", "border": "1px solid #10B981", "padding": "8px", "borderRadius": "6px"}
                },
                {
                    "id": "gen-p2",
                    "data": {"label": "Scale Marketing Campaign and Churn"},
                    "position": {"x": 420, "y": 140},
                    "style": {"background": "#1E293D", "color": "#E2E8F0", "border": "1px solid #10B981", "padding": "8px", "borderRadius": "6px"}
                }
            ])
            edges.extend([
                {"id": "e-root-p1", "source": "root", "target": "gen-p1", "animated": True},
                {"id": "e-root-p2", "source": "root", "target": "gen-p2", "animated": True}
            ])
            
            nodes.append({
                "id": "gen-s1",
                "data": {"label": "⚠️ Unmodeled Operating Cost Growth"},
                "position": {"x": 80, "y": 260},
                "style": {"background": "#3B1824", "color": "#FDA4AF", "border": "1px solid #F43F5E", "padding": "8px", "borderRadius": "6px"}
            })
            edges.append({"id": "e-p1-s1", "source": "gen-p1", "target": "gen-s1", "animated": True})
            
            nodes.append({
                "id": "gen-t1",
                "type": "output",
                "data": {"label": "🚨 Negative Economics & Cash Runout Collapse"},
                "position": {"x": 80, "y": 380},
                "style": {"background": "#7F1D1D", "color": "#FEE2E2", "border": "1px solid #EF4444", "padding": "10px", "borderRadius": "6px"}
            })
            edges.append({"id": "e-s1-t1", "source": "gen-s1", "target": "gen-t1", "animated": True})
            
            nodes.append({
                "id": "gen-s2",
                "data": {"label": "⚠️ Competitor Launches Cloned Architecture"},
                "position": {"x": 420, "y": 260},
                "style": {"background": "#3B1824", "color": "#FDA4AF", "border": "1px solid #F43F5E", "padding": "8px", "borderRadius": "6px"}
            })
            edges.append({"id": "e-p2-s2", "source": "gen-p2", "target": "gen-s2", "animated": True})
            
            nodes.append({
                "id": "gen-t2",
                "type": "output",
                "data": {"label": "🚨 Rapid User Attrition to Major Competitors"},
                "position": {"x": 420, "y": 380},
                "style": {"background": "#7F1D1D", "color": "#FEE2E2", "border": "1px solid #EF4444", "padding": "10px", "borderRadius": "6px"}
            })
            edges.append({"id": "e-s2-t2", "source": "gen-s2", "target": "gen-t2", "animated": True})
            
        return {
            "nodes": nodes,
            "edges": edges
        }

consequence_tree_generator = ConsequenceTreeGenerator()
