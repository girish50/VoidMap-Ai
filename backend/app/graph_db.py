import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import networkx as nx
from neo4j import GraphDatabase

from app.config import settings

logger = logging.getLogger("voidmap.graph")
logging.basicConfig(level=logging.INFO)

class GraphDBManager:
    """
    VOIDMAP Graph Database Manager.
    Manages connection pools to a real Neo4j database instance.
    Includes a robust local NetworkX fallback if the Neo4j server is offline.
    """
    def __init__(self):
        self.driver = None
        self.is_connected = False
        self.local_graph = nx.DiGraph()
        
        # Always build the local fallback graph on initialization
        self._load_local_graph_data()
        
        # Attempt real Neo4j connection if local fallbacks aren't forced
        if not settings.FORCE_LOCAL_FALLBACKS:
            try:
                logger.info(f"Attempting connection to Neo4j at {settings.NEO4J_URI}...")
                self.driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
                # Verify connectivity
                self.driver.verify_connectivity()
                self.is_connected = True
                logger.info("Successfully established connection to Neo4j Database.")
            except Exception as e:
                logger.warning(
                    f"Could not connect to Neo4j ({e}). "
                    "VOIDMAP will automatically utilize local in-memory Graph Engine (NetworkX) fallback."
                )
                self.is_connected = False
        else:
            logger.info("FORCE_LOCAL_FALLBACKS is active. Running exclusively in NetworkX local mode.")
            self.is_connected = False

    def _load_local_graph_data(self):
        """
        Loads expectations from expected_graphs.json and populates the local NetworkX graph.
        """
        try:
            data_file = Path(__file__).parent / "data" / "expected_graphs.json"
            if not data_file.exists():
                logger.error(f"expected_graphs.json not found at {data_file}!")
                return
                
            with open(data_file, "r") as f:
                domain_data: Dict[str, List[Dict[str, Any]]] = json.load(f)
                
            for domain_name, requirements in domain_data.items():
                # Add domain node
                self.local_graph.add_node(domain_name, type="Domain", name=domain_name)
                
                for req in requirements:
                    req_name = req["requirement"]
                    # Add requirement node
                    self.local_graph.add_node(
                        req_name,
                        type="Requirement",
                        name=req_name,
                        category=req["category"],
                        description=req["description"],
                        risk=req["risk"]
                    )
                    # Add link from Domain to Requirement
                    self.local_graph.add_edge(domain_name, req_name, type="REQUIRES")
                    
                    # Add dependencies
                    for dep in req.get("dependencies", []):
                        if dep not in self.local_graph:
                            self.local_graph.add_node(dep, type="Requirement", name=dep)
                        # Add dependency edge
                        self.local_graph.add_edge(req_name, dep, type="DEPENDS_ON")
            logger.info(
                f"Successfully parsed expected_graphs.json. "
                f"Local Graph populated with {self.local_graph.number_of_nodes()} nodes and "
                f"{self.local_graph.number_of_edges()} edges."
            )
        except Exception as e:
            logger.error(f"Failed to load local NetworkX graph: {e}")

    def get_domain_requirements(self, domain: str) -> List[Dict[str, Any]]:
        """
        Retrieves all expected requirement nodes and relationships for a specific domain.
        Uses Cypher if connected to Neo4j, else traverses the local NetworkX graph.
        """
        if self.is_connected and not settings.FORCE_LOCAL_FALLBACKS:
            try:
                # Query expectations via Cypher
                query = """
                MATCH (d:Domain {name: $domain})-[:REQUIRES]->(r:Requirement)
                OPTIONAL MATCH (r)-[:DEPENDS_ON]->(dep:Requirement)
                RETURN r.name AS requirement, 
                       r.category AS category, 
                       r.description AS description, 
                       r.risk AS risk, 
                       collect(dep.name) AS dependencies
                """
                with self.driver.session() as session:
                    result = session.run(query, domain=domain)
                    records = []
                    for record in result:
                        records.append({
                            "requirement": record["requirement"],
                            "category": record["category"],
                            "description": record["description"],
                            "risk": record["risk"],
                            "dependencies": record["dependencies"]
                        })
                    if records:
                        return records
            except Exception as e:
                logger.error(f"Neo4j Cypher query failed: {e}. Falling back to NetworkX.")
        
        # NetworkX Fallback traversal
        if domain not in self.local_graph:
            return []
            
        records = []
        # Find all outgoing nodes from the domain node with relation "REQUIRES"
        for req in self.local_graph.successors(domain):
            node_data = self.local_graph.nodes[req]
            if node_data.get("type") == "Requirement":
                # Find all dependencies for this requirement node
                dependencies = []
                for dep in self.local_graph.successors(req):
                    edge_data = self.local_graph.edges[req, dep]
                    if edge_data.get("type") == "DEPENDS_ON":
                        dependencies.append(dep)
                        
                records.append({
                    "requirement": node_data["name"],
                    "category": node_data.get("category", "General"),
                    "description": node_data.get("description", ""),
                    "risk": node_data.get("risk", ""),
                    "dependencies": dependencies
                })
        return records

    def seed_graph_database(self) -> bool:
        """
        Seeds the real Neo4j database using expected_graphs.json catalog.
        Returns True if successful, else False.
        """
        if not self.is_connected:
            logger.warning("Neo4j database is offline. Cannot seed.")
            return False
            
        try:
            data_file = Path(__file__).parent / "data" / "expected_graphs.json"
            with open(data_file, "r") as f:
                domain_data = json.load(f)
                
            # Cypher schema seeding
            with self.driver.session() as session:
                # Clear existing nodes to prevent duplicates
                session.run("MATCH (n) DETACH DELETE n")
                
                for domain_name, requirements in domain_data.items():
                    # Create Domain node
                    session.run("MERGE (d:Domain {name: $name})", name=domain_name)
                    
                    for req in requirements:
                        # Create Requirement node
                        session.run("""
                            MERGE (r:Requirement {name: $name})
                            ON CREATE SET r.category = $category,
                                          r.description = $description,
                                          r.risk = $risk
                            ON MATCH SET r.category = $category,
                                         r.description = $description,
                                         r.risk = $risk
                        """, 
                        name=req["requirement"],
                        category=req["category"],
                        description=req["description"],
                        risk=req["risk"])
                        
                        # Create relationship: Domain -REQUIRES-> Requirement
                        session.run("""
                            MATCH (d:Domain {name: $d_name})
                            MATCH (r:Requirement {name: $r_name})
                            MERGE (d)-[:REQUIRES]->(r)
                        """, d_name=domain_name, r_name=req["requirement"])
                        
                        # Create relationships for dependencies
                        for dep_name in req.get("dependencies", []):
                            session.run("MERGE (dep:Requirement {name: $name})", name=dep_name)
                            session.run("""
                                MATCH (r:Requirement {name: $r_name})
                                MATCH (dep:Requirement {name: $dep_name})
                                MERGE (r)-[:DEPENDS_ON]->(dep)
                            """, r_name=req["requirement"], dep_name=dep_name)
            logger.info("Successfully seeded Neo4j Database with all expectation nodes and relationships.")
            return True
        except Exception as e:
            logger.error(f"Failed to seed Neo4j Database: {e}")
            return False

    def close(self):
        """
        Closes the active connection pool.
        """
        if self.driver:
            self.driver.close()
            logger.info("Neo4j database connection pool closed.")

# Global Singleton instance
graph_db = GraphDBManager()
