# KRAG: A Knowledge-Graph-based RAG Implementation

This project implements an advanced Retrieval-Augmented Generation (RAG) system that leverages a hybrid search approach, combining semantic vector search with a structured knowledge graph. It is designed to ingest complex documents, such as academic papers, and transform them into a rich, queryable network of information.

## 1. Core Architecture

The system is built on a robust, containerized architecture orchestrated with Docker Compose. This ensures that the environment is reproducible, scalable, and easy to manage. The architecture consists of two primary data backends and a Python-based ingestion and query layer.

- **Qdrant (Vector Database)**: Handles the semantic search component. Text from ingested documents is converted into vector embeddings and stored in Qdrant. This allows for finding text chunks that are conceptually similar to a user's query, even if they don't share keywords.

- **Neo4j (Graph Database)**: Forms the structured knowledge backbone of the system. Instead of treating documents as isolated blocks of text, we use an LLM to extract key entities (like authors, concepts, and other papers) and the relationships between them. This information is modeled as a graph, enabling complex queries that traverse these relationships (e.g., "Find all papers by Author X that discuss Concept Y").

- **Python Application Layer**: A set of Python scripts that act as the glue for the system:
    - `ingest_paper.py`: A powerful pipeline that extracts text from PDFs, uses an LLM to identify entities, and populates both Qdrant and Neo4j.
    - `query_krag.py`: A query engine that performs a hybrid search across both databases to retrieve a rich, combined context for any given query.

![Architecture Diagram](https://i.imgur.com/your-architecture-diagram.png)  <!-- Placeholder for a diagram -->

## 2. Installation and Setup

This project is fully containerized, so the only prerequisite is to have **Docker** and **Docker Compose** installed on your system.

**Step-by-step guide:**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/gptprojectmanager/KRAG.git
    cd KRAG
    ```

2.  **Configure Environment Variables:**
    Copy the example environment file and add your OpenAI API key. This key is essential for the entity extraction step.
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file and replace `your_openai_api_key_here` with your actual key.

3.  **Launch the Infrastructure:**
    Start all the necessary services (Qdrant and Neo4j) using Docker Compose.
    ```bash
    docker-compose up -d
    ```
    This command will download the necessary Docker images and start the database containers in the background.

4.  **Install Python Dependencies:**
    Install the required Python libraries for the ingestion and query scripts.
    ```bash
    pip3 install -r requirements.txt
    ```

## 3. How to Use

### Ingesting a Document

1.  Place the PDF file you want to ingest into the `papers` directory (create it if it doesn't exist).
2.  Run the ingestion script from the project root, passing the path to the paper:
    ```bash
    python3 ingest_paper.py papers/your_paper_name.pdf
    ```
    The script will print its progress as it extracts text, calls the OpenAI API, and populates the databases.

### Querying the Knowledge Graph

Once you have ingested one or more documents, you can query the system using the `query_krag.py` script:
```bash
python3 query_krag.py "your query about the papers"
```

**Example Query:**
```bash
python3 query_krag.py "What is the role of automated market makers?"
```

## 4. Work Completed

- **Robust Infrastructure**: Established a stable, multi-container Docker environment for all backend services, ensuring easy setup and portability.
- **Hybrid Data Storage**: Successfully integrated Qdrant for vector search and Neo4j for graph-based relationships.
- **End-to-End Ingestion Pipeline**: Created a script that automates the entire process of document ingestion: PDF text extraction, LLM-based entity and concept extraction, and population of both databases.
- **Hybrid Query Engine**: Developed a script that demonstrates the power of the hybrid approach by querying both Qdrant and Neo4j to retrieve a comprehensive context.
- **Secure Configuration**: Ensured that sensitive information like API keys is handled securely using `.env` files and is explicitly ignored by Git.

## 5. Comparison and Future Work

This project provides a powerful foundation that is more advanced than many standard RAG implementations.

### Comparison to Other Repositories

- **vs. HKUDS/RAG-Anything**: While `RAG-Anything` is a versatile system, it is a more traditional, document-based RAG. Our KRAG project surpasses this by creating a structured knowledge graph, which allows for a deeper understanding and more complex querying of the document's content.
- **vs. coleam00/PydanticAI-Research-Agent**: This repository is a good example of a research agent, but it does not focus on building a persistent, queryable knowledge graph. KRAG is designed to build a long-term, evolving knowledge base.
- **vs. n8n-and-code-rag**: This project uses n8n to automate a standard RAG workflow on code. KRAG is more flexible, handling complex documents like academic papers, and its knowledge graph provides a richer context than a simple vector store.

### Future Enhancements

The current implementation is a solid proof-of-concept. Here are some ways it could be extended:

- **Advanced Entity Extraction**: Use a more sophisticated LLM prompting strategy to extract not just authors and concepts, but also methodologies, datasets used, and citations of other papers, creating an even richer graph.
- **Recursive Ingestion**: When a paper is ingested, automatically search for and ingest the papers it cites, creating a multi-level, interconnected library.
- **Web UI / API**: Build a simple web interface (e.g., with Flask or FastAPI) to make the ingestion and query process more user-friendly, including a visualization of the knowledge graph for a given query.
- **Integration with Pandoc**: While we initially planned to use Pandoc, we found that a direct-to-text extraction with `PyMuPDF` was more reliable for this workflow. A future enhancement could be to build a more robust document conversion service (potentially using Pandoc in a separate container) to handle a wider variety of formats like `.docx`, `.html`, and `.epub`.