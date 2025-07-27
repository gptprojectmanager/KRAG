
# KRAG: Knowledge-Graph-based RAG Project

Questo progetto ha l'obiettivo di costruire un sistema avanzato di Retrieval-Augmented Generation (RAG) basato su un grafo di conoscenza (Knowledge Graph). L'architettura è progettata per analizzare documenti complessi, come paper accademici, estraendo non solo il testo ma anche le entità e le relazioni tra di esse (es. citazioni, autori, concetti).

## Architettura

Il sistema si basa sulla combinazione di tre componenti principali:

1.  **Pandoc**: Utilizzato come strumento di ingestione universale per convertire vari formati di documenti (PDF, DOCX, LaTeX, etc.) in un formato strutturato e pulito.
2.  **`graphiti_mcp_server` con Neo4j**: Il cuore del sistema. Utilizza un database a grafo (Neo4j) per costruire e memorizzare un grafo di conoscenza a partire dai documenti ingeriti. Questo permette di mappare e interrogare le relazioni complesse all'interno dei dati.
3.  **Qdrant**: Un database vettoriale ad alte prestazioni che memorizza gli "embeddings" del testo, abilitando una ricerca semantica efficiente per trovare informazioni concettualmente rilevanti.

## Stato del Progetto

### Progressi Attuali

-   [x] **Setup del Progetto**: Creata la cartella di progetto `KRAG`.
-   [x] **Setup Repository**: Inizializzata una repository Git locale e collegata a una repository remota su GitHub: [https://github.com/gptprojectmanager/KRAG](https://github.com/gptprojectmanager/KRAG).
-   [x] **Configurazione Ambiente**: Verificata e completata l'installazione di `pandoc` e della libreria Python `PyMuPDF`.
-   [x] **Script di Ingestione Iniziale**: Creato lo script `ingest_paper.py`, in grado di estrarre con successo il testo da un file PDF.
-   [x] **Versionamento**: Il codice iniziale è stato committato e caricato sulla repository GitHub.

### Prossimi Passi

-   [ ] **Avvio dei Servizi**: Verificare che i server `graphiti_mcp_server`, `neo4j` e `qdrant` siano attivi e raggiungibili.
-   [ ] **Integrazione con il Grafo**: Modificare `ingest_paper.py` per inviare il testo estratto al `graphiti_mcp_server`, che lo elaborerà per popolare il grafo di conoscenza.
-   [ ] **Sviluppo Query**: Creare uno script o una funzione per interrogare il grafo e recuperare le informazioni strutturate.
-   [ ] **Costruzione Pipeline RAG**: Integrare il recupero delle informazioni dal grafo con un modello linguistico (LLM) per generare risposte contestuali e accurate basate sui documenti.
