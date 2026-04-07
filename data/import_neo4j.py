"""
Neo4j 数据导入脚本
从 JSON 文件导入节点和关系到 Neo4j
"""

import json
import os
from neo4j import GraphDatabase

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:17687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

def import_data():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    data_dir = os.path.dirname(__file__)
    
    # Load nodes
    with open(os.path.join(data_dir, "neo4j_nodes.json"), encoding="utf-8") as f:
        nodes = json.load(f)
    
    # Load relationships
    with open(os.path.join(data_dir, "neo4j_rels.json"), encoding="utf-8") as f:
        rels = json.load(f)
    
    print(f"Importing {len(nodes)} nodes and {len(rels)} relationships...")
    
    with driver.session() as s:
        # Clear existing data
        print("Clearing existing data...")
        s.run("MATCH (n) DETACH DELETE n")
        
        # Import nodes
        for i, node in enumerate(nodes):
            labels = ":".join(node["labels"]) if node["labels"] else "Entity"
            props = node["props"]
            if props:
                prop_str = ", ".join([f"n.{k} = ${k}" for k in props.keys()])
                cypher = f"CREATE (n:{labels} {{{prop_str}}})"
                s.run(cypher, **props)
            else:
                s.run(f"CREATE (n:{labels})")
            if (i + 1) % 500 == 0:
                print(f"  Nodes: {i + 1}/{len(nodes)}")
        
        print(f"Imported {len(nodes)} nodes")
        
        # Import relationships
        for i, rel in enumerate(rels):
            if not rel["src"] or not rel["dst"]:
                continue
            rel_type = rel["rel_type"]
            props = rel.get("rel_props", {}) or {}
            props["source"] = rel.get("source", "")
            
            prop_str = ", ".join([f"r.{k} = ${k}" for k in props.keys()]) if props else ""
            if prop_str:
                cypher = f"""
                MATCH (a {{name: $src}})
                MATCH (b {{name: $dst}})
                CREATE (a)-[r:{rel_type} {{{prop_str}}}]->(b)
                """
            else:
                cypher = f"""
                MATCH (a {{name: $src}})
                MATCH (b {{name: $dst}})
                CREATE (a)-[r:{rel_type}]->(b)
                SET r.source = $source
                """
            params = {"src": rel["src"], "dst": rel["dst"], **props}
            try:
                s.run(cypher, **params)
            except Exception as e:
                print(f"Error importing rel {rel['src']} -> {rel['dst']}: {e}")
            
            if (i + 1) % 500 == 0:
                print(f"  Relationships: {i + 1}/{len(rels)}")
        
        print(f"Imported {len(rels)} relationships")
    
    driver.close()
    print("Done!")

if __name__ == "__main__":
    import_data()
