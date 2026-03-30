"""
Aplicación Streamlit para exploración visual de documentos técnicos.

Esta aplicación proporciona:
- Visualización interactiva de clusters de documentos
- Búsqueda semántica
- Detección de anomalías
- Clasificación de calidad
"""

import streamlit as st
import numpy as np
from numpy.typing import NDArray
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
from pathlib import Path

# Imports del proyecto
from domain.services.embedding_service import TechnicalDocEmbeddingService
from domain.services.anomaly_detection import (
    IsolationForestDetector,
    create_anomaly_detector,
)
from domain.services.quality_classifier import (
    QualityClassifier,
    QualityLabel,
    create_quality_classifier,
)
from domain.services.clustering import (
    DocumentClusterer,
    VisualizationService,
    ClusterAnalysis,
)
from infrastructure.persistence.chroma_repository import ChromaDocumentRepository
from infrastructure.file_handlers import (
    MarkdownHandler,
    RSTHandler,
    PDFHandler,
    TextHandler,
)
from domain.entities import TechnicalDocument, DocumentType


# Page configuration
st.set_page_config(
    page_title="Technical Documents Explorer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS with dark library background
st.markdown(
    """
<style>
/* Dark library background with books */
.stApp {
    background-image: linear-gradient(rgba(20, 25, 30, 0.92), rgba(30, 35, 40, 0.95)), url('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=70');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Make content background solid dark */
.main .block-container {
    background-color: #1a1a2e;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #16213e;
}

/* Typography - light colors for dark background */
.stTitle, h1, h2, h3 {
    color: #e8e8e8 !important;
}

.stMarkdown, p, div {
    color: #d0d0d0 !important;
}

/* Tabs styling for dark mode */
.stTabs {
    background-color: transparent;
}

/* Custom styling */
.sidebar-section {
    padding: 10px;
    margin-bottom: 10px;
}
.student-name {
    font-size: 28px;
    font-weight: bold;
    color: #ffd700;
    text-align: center;
    padding: 15px 10px;
}
.student-role {
    font-size: 16px;
    color: #b0b0b0;
    text-align: center;
    margin-bottom: 15px;
}
.social-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 15px 0;
}
.social-link {
    display: inline-flex;
    align-items: center;
    padding: 10px 20px;
    background-color: #ffd700;
    color: #1a1a2e;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
}
.social-link.linkedin {
    background-color: #0077b5;
    color: white;
}
.project-title {
    font-size: 12px;
    color: #a0a0a0;
    text-align: center;
    margin-top: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)


class DocumentExplorerApp:
    """Main application for document exploration"""

    def __init__(self, db_path: str = "data/tech_docs_db"):
        self.db_path = db_path
        self._initialize_services()

    def _initialize_services(self) -> None:
        """Inicializa los servicios necesarios"""
        with st.spinner("Loading models..."):
            try:
                self.embedding_service = TechnicalDocEmbeddingService()
                self.repo = ChromaDocumentRepository(self.db_path)
                self.anomaly_detector = create_anomaly_detector(
                    "isolation_forest", contamination=0.1
                )
                self.quality_classifier = create_quality_classifier("random_forest")
                self.clusterer = DocumentClusterer(n_clusters=5)
                self.visualizer = VisualizationService()
                st.success("✓ Models loaded successfully")
            except Exception as e:
                st.error(f"Error loading models: {str(e)}")
                self.embedding_service = None
                self.repo = None

    def load_documents(self) -> Tuple[List[TechnicalDocument], NDArray[np.float32]]:
        """Load documents and their embeddings"""
        if self.repo is None:
            return [], np.array([])

        # Obtener todos los documentos
        try:
            # ChromaDB no tiene get_all, usamos una búsqueda grande
            results = self.repo.collection.get()

            documents = []
            embeddings = []

            if results["ids"] and len(results["ids"]) > 0:
                for i in range(len(results["ids"])):
                    doc = TechnicalDocument(
                        id=results["ids"][i],
                        content=results["documents"][i],
                        title=results["metadatas"][i].get("title", "Unknown"),
                        file_path=results["metadatas"][i].get("file_path", ""),
                        document_type=DocumentType(
                            results["metadatas"][i].get("type", "markdown")
                        ),
                    )
                    documents.append(doc)

                    # Generar embedding
                    emb = self.embedding_service.generate_document_embedding(doc)
                    embeddings.append(emb)

            return documents, np.array(embeddings)
        except Exception as e:
            st.error(f"Error loading documents: {str(e)}")
            return [], np.array([])

    def run(self) -> None:
        """Run the application"""
        st.title("📚 Technical Documents Explorer")
        st.markdown(
            "Explore your document corpus with interactive visualization and quality analysis"
        )

        # Sección para subir documentos
        with st.expander("📤 Upload documents", expanded=False):
            uploaded_files = st.file_uploader(
                "Select PDF, Markdown, RST or text files",
                type=["pdf", "md", "rst", "txt"],
                accept_multiple_files=True,
            )

            if uploaded_files:
                if st.button("Process uploaded documents"):
                    with st.spinner("Processing documents..."):
                        for uploaded_file in uploaded_files:
                            # Guardar archivo temporalmente
                            temp_path = Path("data/temp") / uploaded_file.name
                            temp_path.parent.mkdir(parents=True, exist_ok=True)

                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            # Determinar tipo de archivo
                            ext = temp_path.suffix.lower()
                            handler_class = {
                                ".pdf": PDFHandler,
                                ".md": MarkdownHandler,
                                ".rst": RSTHandler,
                                ".txt": TextHandler,
                            }.get(ext)

                            if handler_class:
                                handler = handler_class(source="uploaded")
                                doc = handler.parse(str(temp_path))

                                if doc and self.embedding_service and self.repo:
                                    embedding = self.embedding_service.generate_document_embedding(
                                        doc
                                    )
                                    self.repo.add_document(doc, embedding)
                                    st.success(f"✓ {uploaded_file.name} processed")

                            # Limpiar archivo temporal
                            temp_path.unlink(missing_ok=True)

                        st.rerun()

        # Load data
        documents, embeddings = self.load_documents()

        if len(documents) == 0:
            st.warning("No documents found. Run the ingestion pipeline first.")
            st.code(
                "python -m src.interfaces.cli.main process data/documents",
                language="bash",
            )
            return

        st.info(f"📄 {len(documents)} documents loaded")

        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🔍 Cluster Visualization",
                "📊 Quality Analysis",
                "⚠️ Anomaly Detection",
                "🔎 Semantic Search",
            ]
        )

        with tab1:
            self._render_cluster_visualization(documents, embeddings)

        with tab2:
            self._render_quality_analysis(documents, embeddings)

        with tab3:
            self._render_anomaly_detection(documents, embeddings)

        with tab4:
            self._render_semantic_search(documents)

    def _render_cluster_visualization(
        self, documents: List[TechnicalDocument], embeddings: NDArray[np.float32]
    ) -> None:
        """Renderiza la visualización de clusters"""
        st.header("Cluster Visualization")

        n_docs = len(documents)
        if n_docs < 2:
            st.warning("At least 2 documents required for clustering")
            return

        col1, col2 = st.columns([3, 1])

        with col2:
            st.subheader("Settings")
            max_clusters = min(10, n_docs)
            n_clusters = st.slider(
                "Number of Clusters", 2, max_clusters, min(5, n_docs)
            )
            method = st.selectbox("Dimensionality Reduction", ["tsne", "pca", "mds"])

            # Re-calcular clusters
            self.clusterer = DocumentClusterer(n_clusters=n_clusters)
            labels = self.clusterer.fit_predict(embeddings)

            # Reducir dimensiones
            coords_2d = self.visualizer.reduce_dimensions(
                embeddings, n_components=2, method=method
            )

        with col1:
            # Crear DataFrame para visualización
            df = pd.DataFrame(
                {
                    "x": coords_2d[:, 0],
                    "y": coords_2d[:, 1],
                    "cluster": labels,
                    "title": [doc.title for doc in documents],
                }
            )

            # Visualización con Altair
            st.subheader("Documents Map")

            # Scatter plot interactivo
            chart = st.scatter_chart(data=df, x="x", y="y", color="cluster", height=500)

            # Mostrar detalles al hacer click (simplificado)
            st.subheader("Cluster Details")

            # Estadísticas de clusters
            stats = ClusterAnalysis.get_cluster_stats(embeddings, labels)
            stats_df = pd.DataFrame(stats)
            st.dataframe(stats_df, use_container_width=True)

            # Distribución
            distribution = ClusterAnalysis.get_cluster_distribution(labels)
            st.write("Distribution:", distribution)

    def _render_quality_analysis(
        self, documents: List[TechnicalDocument], embeddings: NDArray[np.float32]
    ) -> None:
        """Renderiza el análisis de calidad"""
        st.header("Quality Analysis")

        st.info("📝 The quality classifier requires labeled training data.")
        st.markdown(
            """
        To train the quality model, you need:
        1. A set of manually labeled documents
        2. Labels: `high`, `medium`, `low`
        
        Use the training function provided below.
        """
        )

        # Sección de entrenamiento
        with st.expander("🎓 Train Quality Model"):
            st.write("Train the classifier with labeled data")

            # Simular datos de entrenamiento (en producción vendría de etiquetas reales)
            if st.button("Train with sample data"):
                # Crear etiquetas simuladas basadas en longitud del contenido
                labels = []
                for doc in documents:
                    content_len = len(doc.content)
                    if content_len > 5000:
                        labels.append(QualityLabel.HIGH)
                    elif content_len > 1000:
                        labels.append(QualityLabel.MEDIUM)
                    else:
                        labels.append(QualityLabel.LOW)

                self.quality_classifier.fit(embeddings, labels)
                st.success("Model trained successfully")

                # Predicciones
                predictions = self.quality_classifier.predict_batch(embeddings)

                # Mostrar resultados
                results = []
                for doc, pred in zip(documents, predictions):
                    results.append({"Documento": doc.title[:50], "Calidad": pred})

                st.dataframe(pd.DataFrame(results))

        # Mostrar distribución de calidad si hay modelo entrenado
        if (
            hasattr(self.quality_classifier, "_is_fitted")
            and self.quality_classifier._is_fitted
        ):
            st.subheader("Resultados del Análisis")
            predictions = self.quality_classifier.predict_batch(embeddings)

            quality_dist = pd.Series(predictions).value_counts()
            st.bar_chart(quality_dist)

    def _render_anomaly_detection(
        self, documents: List[TechnicalDocument], embeddings: NDArray[np.float32]
    ) -> None:
        """Renderiza la detección de anomalías"""
        st.header("Anomaly Detection")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Settings")

            detector_type = st.selectbox("Detector type", ["isolation_forest", "lof"])

            contamination = st.slider(
                "Expected contamination (anomaly proportion)", 0.01, 0.5, 0.1
            )

            if st.button("Detect Anomalies"):
                with st.spinner("Analyzing documents..."):
                    detector = create_anomaly_detector(
                        detector_type, contamination=contamination
                    )
                    predictions = detector.fit_predict(embeddings)
                    scores = detector.get_anomaly_scores(embeddings)

                    # Guardar en session state
                    st.session_state["anomaly_predictions"] = predictions
                    st.session_state["anomaly_scores"] = scores

                    # Contar anomalías
                    n_anomalies = (predictions == 1).sum()
                    st.success(f"✓ {n_anomalies} anomalies detected")

        with col2:
            if "anomaly_predictions" in st.session_state:
                predictions = st.session_state["anomaly_predictions"]
                scores = st.session_state["anomaly_scores"]

                # Distribución
                unique, counts = np.unique(predictions, return_counts=True)
                dist = dict(zip(unique, counts))

                st.metric("Normales", dist.get(-1, 0))
                st.metric("Anómalos", dist.get(1, 0))

        # Lista de anomalías
        if "anomaly_predictions" in st.session_state:
            st.subheader("Anomalous Documents")

            predictions = st.session_state["anomaly_predictions"]
            scores = st.session_state["anomaly_scores"]

            # Filtrar anomalías
            anomaly_docs = []
            for i, (doc, pred, score) in enumerate(zip(documents, predictions, scores)):
                if pred == 1:
                    anomaly_docs.append(
                        {
                            "Título": doc.title[:50],
                            "Score": f"{score:.3f}",
                            "Tipo": doc.document_type.value,
                        }
                    )

            if anomaly_docs:
                st.dataframe(pd.DataFrame(anomaly_docs), use_container_width=True)
            else:
                st.info("No anomalous documents found")

    def _render_semantic_search(self, documents: List[TechnicalDocument]) -> None:
        """Renderiza la búsqueda semántica"""
        st.header("🔎 Semantic Search")

        query = st.text_input(
            "Enter your query:", placeholder="Example: how to configure API..."
        )

        col1, col2 = st.columns([1, 4])

        with col1:
            top_k = st.slider("Number of results", 1, 20, 5)

        if query and self.embedding_service and self.repo:
            with st.spinner("Buscando..."):
                # Generar embedding de la query
                query_embedding = self.embedding_service.generate_embedding(query)

                # Buscar en la base de datos
                results = self.repo.search_similar(query_embedding, top_k=top_k)

                st.subheader(f"Resultados para: '{query}'")

                for i, doc in enumerate(results, 1):
                    with st.container():
                        st.markdown(f"**{i}. {doc.title}**")
                        st.caption(f"📄 {doc.document_type.value} | 📁 {doc.file_path}")
                        st.write(doc.content[:300] + "...")
                        st.divider()

        elif query:
            st.warning("Load documents first")


def main():
    """Main entry point"""
    # Custom CSS for better styling
    st.markdown(
        """
    <style>
    .sidebar-section {
        padding: 10px;
        margin-bottom: 10px;
    }
    .student-name {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A5F;
        text-align: center;
        padding: 15px 10px;
    }
    .student-role {
        font-size: 16px;
        color: #666;
        text-align: center;
        margin-bottom: 15px;
    }
    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 15px 0;
    }
    .social-link {
        display: inline-flex;
        align-items: center;
        padding: 10px 20px;
        background-color: #24292e;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
    }
    .social-link.linkedin {
        background-color: #0077b5;
    }
    .project-title {
        font-size: 12px;
        color: #888;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar settings
    st.sidebar.title("⚙️ Settings")

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        '<div class="student-name">ALEJANDRA LOPEZ</div>', unsafe_allow_html=True
    )
    st.sidebar.markdown(
        '<div class="student-role">Software Engineer</div>', unsafe_allow_html=True
    )

    # Social links styled as buttons
    st.sidebar.markdown(
        """
    <div class="social-links">
        <a href="https://github.com/Alejandra-Lopez17" target="_blank" class="social-link">GitHub</a>
        <a href="https://www.linkedin.com/in/alejandra-lopez1707/" target="_blank" class="social-link linkedin">LinkedIn</a>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        '<div class="project-title">Data Science and Machine Learning Vault</div>',
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    db_path = st.sidebar.text_input("Database path", "data/tech_docs_db")

    # Run application
    app = DocumentExplorerApp(db_path)
    app.run()


if __name__ == "__main__":
    main()
# formatted
