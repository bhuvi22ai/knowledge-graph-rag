import os
import requests
import certifi

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Configure trusted certificates for Neo4j
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

# Load database settings
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


def retrieve_facts():
    """Retrieve relationships stored in Neo4j."""

    query = """
    MATCH (source)-[r]->(target)
    RETURN source.name AS source,
           type(r) AS relationship,
           target.name AS target
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        with driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]


def generate_answer(question, facts):
    """Generate an answer using Ollama and graph facts."""

    context = "\n".join(
        f"{fact['source']} --{fact['relationship']}--> "
        f"{fact['target']}"
        for fact in facts
    )

    prompt = f"""
You are a helpful Knowledge Graph RAG assistant.

Answer the question using only the facts provided below.
Do not invent facts or add unsupported information.
If the facts do not contain the answer, say:
"I could not find that information in the knowledge graph."

Knowledge graph facts:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=180
    )

    response.raise_for_status()
    return response.json()["response"].strip()


if __name__ == "__main__":
    if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
        raise ValueError("Missing Neo4j settings in .env")

    question = input("Ask a question about the graph: ")

    try:
        facts = retrieve_facts()

        if not facts:
            print("No facts found in the knowledge graph.")
        else:
            answer = generate_answer(question, facts)
            print("\nAnswer:")
            print(answer)

    except Exception as error:
        print(f"Application error: {type(error).__name__}: {error}")