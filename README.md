# Knowledge Graph RAG

A beginner-friendly Proof of Concept (POC) that combines a Neo4j knowledge graph with a locally running LLM to answer questions using stored relationships.

## Overview

This project demonstrates a simple Knowledge Graph Retrieval-Augmented Generation (Graph RAG) workflow:

1. Store entities and relationships in Neo4j AuraDB.
2. Retrieve graph facts using Cypher queries.
3. Pass the retrieved facts to a local LLM through Ollama.
4. Generate answers grounded in the retrieved facts.
5. Return a fallback response when the graph does not contain the answer.

## Technology Stack

- **Python** — application logic
- **Neo4j AuraDB** — graph database
- **Cypher** — graph query language
- **Ollama** — local LLM inference
- **Llama 3.2 1B** — language model
- **Requests** — Ollama API calls
- **python-dotenv** — environment variable loading

## Project Structure

```text
KnowledgeGraphRAG/
├── app.py
├── setup_graph.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.12
- A Neo4j AuraDB instance
- Ollama installed locally
- Git

## Setup

1. Clone the repository and enter the project directory.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file using `.env.example` and fill in your own Neo4j credentials.
5. Download the model:

   ```bash
   ollama pull llama3.2:1b
   ```

6. Create the sample graph:

   ```bash
   python setup_graph.py
   ```

7. Run the application:

   ```bash
   python app.py
   ```

## Example

Question:

`Which technologies does the project use?`

Expected answer:

`The project uses Python and Neo4j.`

The exact wording may vary depending on the model.

## Current Scope and Limitations

This is a learning POC with a small, manually created graph. It demonstrates graph retrieval and grounded answer generation; it does not yet include document ingestion, automatic entity extraction, or advanced retrieval strategies.

## Security

- Never commit your `.env` file or database credentials.
- Use your own Neo4j credentials in your local environment.
- Keep `.env` excluded through `.gitignore`.
