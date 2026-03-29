"""
Clustering and visualization module for technical documents.

Provides unsupervised clustering and visualization
of documents in the embedding space.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from numpy.typing import NDArray
import logging
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.manifold import TSNE, MDS
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class IClusterer(ABC):
    """Interface for clustering algorithms"""
    
    @abstractmethod
    def fit_predict(self, embeddings: NDArray[np.float32]) -> NDArray[np.int32]:
        """Fit and predict clusters"""
        pass
    
    @abstractmethod
    def get_cluster_centers(self) -> Optional[NDArray[np.float32]]:
        """Return cluster centers"""


class DocumentClusterer(IClusterer):
    """
    Document clustering using K-Means.
    
    K-Means is a partitioning clustering algorithm that divides documents
    into K groups based on the similarity of their embeddings.
    """
    
    def __init__(
        self,
        n_clusters: int = 5,
        random_state: int = 42,
        n_init: int = 10
    ) -> None:
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.n_init = n_init
        self._model: Optional[KMeans] = None
        self._scaler: Optional[StandardScaler] = None
        
    def fit(self, embeddings: NDArray[np.float32]) -> None:
        """Train the clustering model"""
        try:
            # Scale embeddings for better performance
            self._scaler = StandardScaler()
            embeddings_scaled = self._scaler.fit_transform(embeddings)
            
            self._model = KMeans(
                n_clusters=self.n_clusters,
                random_state=self.random_state,
                n_init=self.n_init
            )
            self._model.fit(embeddings_scaled)
            logger.info(f"K-Means clustering completed with {self.n_clusters} clusters")
        except Exception as e:
            logger.error(f"Error in clustering: {str(e)}")
            raise
    
    def fit_predict(self, embeddings: NDArray[np.float32]) -> NDArray[np.int32]:
        """Fit and predict clusters"""
        self.fit(embeddings)
        return self._model.labels_
    
    def predict(self, embedding: NDArray[np.float32]) -> int:
        """Predict the cluster of a new document"""
        if self._model is None:
            raise ValueError("Model has not been trained yet")
        embedding_scaled = self._scaler.transform(embedding.reshape(1, -1))
        return int(self._model.predict(embedding_scaled)[0])
    
    def get_cluster_centers(self) -> Optional[NDArray[np.float32]]:
        """Return cluster centers"""
        if self._model is None:
            return None
        # Transform centers back to original space
        return self._scaler.inverse_transform(self._model.cluster_centers_)
    
    def get_inertia(self) -> float:
        """Return sum of distances to nearest center (within-cluster sum of squares)"""
        if self._model is None:
            return 0.0
        return float(self._model.inertia_)


class HDBSCANClusterer(IClusterer):
    """
    Clustering using DBSCAN (Density-Based Spatial Clustering).
    
    DBSCAN is a density-based algorithm that can find arbitrarily shaped
    clusters and automatically detect the number of clusters.
    """
    
    def __init__(
        self,
        eps: float = 0.5,
        min_samples: int = 5
    ) -> None:
        self.eps = eps
        self.min_samples = min_samples
        self._model: Optional[DBSCAN] = None
        self._scaler: Optional[StandardScaler] = None
        
    def fit(self, embeddings: NDArray[np.float32]) -> None:
        try:
            self._scaler = StandardScaler()
            embeddings_scaled = self._scaler.fit_transform(embeddings)
            
            self._model = DBSCAN(
                eps=self.eps,
                min_samples=self.min_samples,
                n_jobs=-1
            )
            self._model.fit(embeddings_scaled)
            
            n_clusters = len(set(self._model.labels_)) - (1 if -1 in self._model.labels_ else 0)
            n_noise = list(self._model.labels_).count(-1)
            logger.info(f"DBSCAN: {n_clusters} clusters, {n_noise} noise points")
        except Exception as e:
            logger.error(f"Error in DBSCAN: {str(e)}")
            raise
    
    def fit_predict(self, embeddings: NDArray[np.float32]) -> NDArray[np.int32]:
        self.fit(embeddings)
        return self._model.labels_
    
    def get_cluster_centers(self) -> Optional[NDArray[np.float32]]:
        """DBSCAN doesn't have explicit cluster centers"""
        return None


class VisualizationService:
    """
    Service for visualization of documents in 2D/3D space.
    """
    
    def __init__(self) -> None:
        self._reducer_2d: Optional[TSNE] = None
        self._reducer_3d: Optional[TSNE] = None
        
    def reduce_dimensions(
        self,
        embeddings: NDArray[np.float32],
        n_components: int = 2,
        method: str = "tsne"
    ) -> NDArray[np.float32]:
        """
        Reduce the dimensions of embeddings for visualization.
        
        Args:
            embeddings: High-dimensional embeddings
            n_components: 2 or 3 for visualization
            method: 'tsne', 'pca', or 'mds'
        
        Returns:
            Embeddings reduced to n_components dimensions
        """
        try:
            # Scale embeddings
            scaler = StandardScaler()
            embeddings_scaled = scaler.fit_transform(embeddings)
            
            if method == "pca":
                reducer = PCA(n_components=n_components, random_state=42)
            elif method == "mds":
                reducer = MDS(n_components=n_components, random_state=42, normalized_stress="auto")
            else:  # tsne
                reducer = TSNE(
                    n_components=n_components,
                    random_state=42,
                    perplexity=min(30, len(embeddings) - 1),
                    n_iter=1000
                )
            
            reduced = reducer.fit_transform(embeddings_scaled)
            logger.info(f"Dimensionality reduction to {n_components}D completed with {method}")
            return reduced
            
        except Exception as e:
            logger.error(f"Error in dimensionality reduction: {str(e)}")
            # Return PCA as fallback
            scaler = StandardScaler()
            embeddings_scaled = scaler.fit_transform(embeddings)
            pca = PCA(n_components=min(n_components, embeddings.shape[1]))
            return pca.fit_transform(embeddings_scaled)
    
    def get_2d_coordinates(
        self,
        embeddings: NDArray[np.float32],
        method: str = "tsne"
    ) -> Tuple[NDArray[np.float32], NDArray[np.float32]]:
        """
        Get 2D (x, y) coordinates for visualization.
        
        Returns:
            Tuple of (x, y) arrays
        """
        coords = self.reduce_dimensions(embeddings, n_components=2, method=method)
        return coords[:, 0], coords[:, 1]
    
    def get_3d_coordinates(
        self,
        embeddings: NDArray[np.float32],
        method: str = "tsne"
    ) -> Tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32]]:
        """
        Get 3D (x, y, z) coordinates for visualization.
        
        Returns:
            Tuple of (x, y, z) arrays
        """
        coords = self.reduce_dimensions(embeddings, n_components=3, method=method)
        return coords[:, 0], coords[:, 1], coords[:, 2]


class ClusterAnalysis:
    """
    Cluster analysis to understand the distribution of documents.
    """
    
    @staticmethod
    def get_cluster_distribution(
        labels: NDArray[np.int32]
    ) -> Dict[int, int]:
        """Return distribution of documents per cluster"""
        unique, counts = np.unique(labels, return_counts=True)
        return {int(label): int(count) for label, count in zip(unique, counts)}
    
    @staticmethod
    def get_cluster_stats(
        embeddings: NDArray[np.float32],
        labels: NDArray[np.int32]
    ) -> List[Dict[str, Any]]:
        """Calculate statistics per cluster"""
        stats = []
        unique_labels = np.unique(labels)
        
        for label in unique_labels:
            mask = labels == label
            cluster_embeddings = embeddings[mask]
            
            # Calculate centroid
            centroid = cluster_embeddings.mean(axis=0)
            
            # Calculate radius (max distance to centroid)
            distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
            radius = distances.max()
            
            # Calculate cohesion (mean distance to centroid)
            cohesion = distances.mean()
            
            stats.append({
                "cluster": int(label),
                "size": int(mask.sum()),
                "radius": float(radius),
                "cohesion": float(cohesion),
                "is_noise": label == -1
            })
        
        return stats


def create_clusterer(
    clusterer_type: str = "kmeans",
    **kwargs
) -> IClusterer:
    """
    Factory to create clusterers.
    
    Args:
        clusterer_type: 'kmeans', 'dbscan', or 'agglomerative'
        **kwargs: Additional parameters
    """
    if clusterer_type == "kmeans":
        return DocumentClusterer(**kwargs)
    elif clusterer_type == "dbscan":
        return HDBSCANClusterer(**kwargs)
    else:
        raise ValueError(f"Unknown clusterer type: {clusterer_type}")