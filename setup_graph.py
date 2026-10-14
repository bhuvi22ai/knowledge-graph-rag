import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

if not all([uri, username, password]):
    raise ValueError("Missing Neo4j settings in .env")

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)

query = """
MERGE (p:Project {name: 'Knowledge Graph RAG'})
MERGE (t1:Technology {name: 'Python'})
MERGE (t2:Technology {name: 'Neo4j'})
MERGE (c:Capability {name: 'Graph Search'})

MERGE (p)-[:USES]->(t1)
MERGE (p)-[:USES]->(t2)
MERGE (t2)-[:SUPPORTS]->(c)
"""

try:
    driver.verify_connectivity()

    with driver.session() as session:
        session.run(query)

    print("Knowledge graph created successfully!")

except Exception as error:
    print("Error:", error)

finally:
    driver.close()