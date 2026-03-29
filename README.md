# Data Science and Machine Learning Vault

The required *Python* version for this project is *3.12.x.*

## About me

My name is **Yovana Alejandra Hinestroza Lopez** and I am currently a student at **Jala University**. I am just getting started in the world of data science and machine learning, and I want to learn and grow in this field.

## Setup environment

As usual setup your virtual environment:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip setuptools
$ pip install -r requirements-dev.txt
$ pip install -e .
```

## Basic code compliance

```
$ black .
All done! ✨ 🍰 ✨
X files left unchanged.
$ mypy .
Success: no issues found in X source files
```

## About the CI/CD pipeline

This `monorepo` comes with a pre-configured CI/CD pipeline that is triggered every time a push is made to a **merge request** or when a **merge request** is integrated into the **main** branch.

The pipeline is configured to:

- Execute **code compliance** checks.
- Generate documentation.

> You may add more stages or jobs to the pipeline, but make sure you **do not remove the existing ones**. In addition, make sure you do your best to **keep the pipeline green** at all times.

## Information for students

When importing your `monorepo` for the first time, please make sure you keep the name of the project as `csds-352-machine-learning-vault` (**all lowercase**) and execute the following checklist:

- [x] Write the **About me** section. Include your name, your email, and feel free to add any other information you want to share. It would be awesome if you can add your expectations for this course.
- [ ] The existing CI/CD pipeline is configured to generate a PDF slide deck intended to be used as a companion document for the course. Please, **update your name and email** in the `documentation/csds-352-vault.typ` file.
- [x] Remove this section from the README file once you have completed the above tasks.

---

# Capstone Project - Technical Documents Explorer

## Domain

**Technical Documentation Management**

This project focuses on building an intelligent system for managing and organizing technical documentation (API guides, tutorials, reference manuals) using machine learning techniques.

## What does this project do?

This project implements an intelligent system for managing and exploring technical documentation using machine learning. It can:

1. **Process documents** - Load PDF, Markdown, RST, and text files
2. **Generate embeddings** - Convert text to vector representations using AI
3. **Cluster documents** - Group similar documents together
4. **Detect anomalies** - Find unusual or irrelevant documents
5. **Classify quality** - Evaluate document quality automatically
6. **Search semantically** - Find documents by meaning, not just keywords

## Data Acquisition

The project uses open-source technical documentation:
- **Source:** Python official documentation, ML tutorials, API guides
- **License:** Open access / MIT License
- **Format:** PDF, Markdown, RST, TXT
- **Location:** `data/documents/`

## Preprocessing Pipeline

1. **File Loading** - Read PDF, Markdown, RST, TXT files
2. **Text Extraction** - Extract content from each document
3. **Embedding Generation** - Convert text to vectors using Sentence Transformers
4. **Vector Storage** - Store embeddings in ChromaDB

## Architecture

```
src/
├── domain/               # Business logic
│   ├── entities/         # Document, Embedding entities
│   ├── repositories/    # Data access interfaces
│   └── services/        # Core services
│       ├── embedding_service.py       # Sentence Transformers
│       ├── anomaly_detection.py      # Isolation Forest, LOF
│       ├── clustering.py             # K-Means, DBSCAN, TSNE
│       ├── quality_classifier.py     # Random Forest
│       └── text_processing.py
├── infrastructure/       # External implementations
│   ├── file_handlers/   # PDF, Markdown, RST, TXT handlers
│   └── persistence/    # ChromaDB implementation
├── interfaces/          # User interfaces
│   ├── cli/             # Command-line interface
│   └── web/             # Streamlit and FastAPI apps
├── api/                 # REST API
└── application/         # Use cases
```

## How to run it

### 1. Process documents
```bash
python -m src.interfaces.cli.main process data/documents
```

### 2. Run the web interface
```bash
streamlit run run_streamlit.py
```

### 3. Run the API
```bash
uvicorn src.interfaces.web.fastapi_app:app --reload
```

## Technologies Used

- **Python 3.12**
- **Sentence Transformers** - Local embedding model (all-mpnet-base-v2)
- **ChromaDB** - Vector database
- **scikit-learn** - ML algorithms (Isolation Forest, Random Forest, K-Means, TSNE)
- **Streamlit** - Web UI
- **FastAPI** - REST API
