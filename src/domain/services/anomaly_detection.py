"""
Anomaly detection module for technical documents.

Uses Isolation Forest to identify anomalous documents in the corpus
based on their vector embeddings.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import numpy as np
from numpy.typing import NDArray
import logging
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

logger = logging.getLogger(__name__)


class IAnomalyDetector(ABC):
    """Interface for anomaly detectors"""
    
    @abstractmethod
    def fit_predict(self, embeddings: NDArray[np.float32]) -> NDArray[np.int32]:
        """Detect anomalies in the given embeddings"""
        pass
    
    @abstractmethod
    def predict(self, embedding: NDArray[np.float32]) -> int:
        """Predict if an embedding is anomalous (1) or normal (-1)"""
        pass


class IsolationForestDetector(IAnomalyDetector):
    """
    Anomaly detector using Isolation Forest.
    
    Isolation Forest is an unsupervised algorithm that identifies anomalies
    based on how easily a point can be "isolated" in the feature space.
    """
    
    def __init__(
        self,
        contamination: float = 0.1,
        n_estimators: int = 100,
        random_state: int = 42
    ) -> None:
        """
        Args:
            contamination: Expected proportion of anomalies in the dataset (0.0 - 0.5)
            n_estimators: Number of trees in the forest
            random_state: Seed for reproducibility
        """
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self._model: Optional[IsolationForest] = None
        self._is_fitted = False
        
    def fit(self, embeddings: NDArray[np.float32]) -> None:
        """Train the model with the given embeddings"""
        try:
            self._model = IsolationForest(
                contamination=self.contamination,
                n_estimators=self.n_estimators,
                random_state=self.random_state,
                n_jobs=-1
            )
            self._model.fit(embeddings)
            self._is_fitted = True
            logger.info(f"Isolation Forest trained with {len(embeddings)} samples")
        except Exception as e:
            logger.error(f"Error training Isolation Forest: {str(e)}")
            raise
            
    def fit_predict(self, embeddings: NDArray[np.float32]) -> NDArray[np.int32]:
        """
        Train and predict anomalies.
        
        Returns:
            Array of -1 (normal) and 1 (anomaly)
        """
        self.fit(embeddings)
        predictions = self._model.predict(embeddings)
        return predictions
    
    def predict(self, embedding: NDArray[np.float32]) -> int:
        """Predict if an embedding is anomalous"""
        if not self._is_fitted:
            raise ValueError("Model has not been trained yet")
        return int(self._model.predict(embedding.reshape(1, -1))[0])
    
    def score_samples(self, embeddings: NDArray[np.float32]) -> NDArray[np.float32]:
        """
        Return anomaly scores (lower = more anomalous)
        """
        if not self._is_fitted:
            raise ValueError("Model has not been trained yet")
        return self._model.score_samples(embeddings)
    
    def get_anomaly_scores(self, embeddings: NDArray[np.float32]) -> List[float]:
        """
        Return normalized anomaly scores from 0 to 1
        (higher = more anomalous)
        """
        raw_scores = self.score_samples(embeddings)
        # Invert and normalize: lower scores (more anomalous) -> higher values
        min_score = raw_scores.min()
        max_score = raw_scores.max()
        if max_score - min_score == 0:
            return [0.5] * len(raw_scores)
        normalized = 1 - (raw_scores - min_score) / (max_score - min_score)
        return normalized.tolist()


class LocalOutlierFactorDetector(IAnomalyDetector):
    """
    Anomaly detector using Local Outlier Factor.
    
    LOF is a density-based algorithm that identifies points that are
    significantly less dense than their neighbors.
    """
    
    def __init__(
        self,
        n_neighbors: int = 20,
        contamination: float = 0.1
    ) -> None:
        self.n_neighbors = n_neighbors
        self.contamination = contamination
        self._model: Optional[LocalOutlierFactor] = None
        self._is_fitted = False
        
    def fit(self, embeddings: NDArray[np.float32]) -> None:
        """Train the model"""
        try:
            # Novelty detection mode (allows prediction after fit)
            self._model = LocalOutlierFactor(
                n_neighbors=self.n_neighbors,
                contamination=self.contamination,
                novelty=True,
                n_jobs=-1
            )
            self._model.fit(embeddings)
            self._is_fitted = True
            logger.info(f"LOF trained with {len(embeddings)} samples")
        except Exception as e:
            logger.error(f"Error training LOF: {str(e)}")
            raise
            
    def fit_predict(self, embeddings: NDArray[np.float32]) -> NDArray[np.int32]:
        self.fit(embeddings)
        # LOF in novelty mode doesn't have fit_predict, use predict
        return self._model.predict(embeddings)
    
    def predict(self, embedding: NDArray[np.float32]) -> int:
        if not self._is_fitted:
            raise ValueError("Model has not been trained yet")
        return int(self._model.predict(embedding.reshape(1, -1))[0])
    
    def get_anomaly_scores(self, embeddings: NDArray[np.float32]) -> List[float]:
        if not self._is_fitted:
            raise ValueError("Model has not been trained yet")
        # score_samples returns negative values (more negative = more anomalous)
        raw_scores = self._model.score_samples(embeddings)
        # Normalize to 0-1 (higher = more anomalous)
        min_score = raw_scores.min()
        max_score = raw_scores.max()
        if max_score - min_score == 0:
            return [0.5] * len(raw_scores)
        normalized = 1 - (raw_scores - min_score) / (max_score - min_score)
        return normalized.tolist()


def create_anomaly_detector(
    detector_type: str = "isolation_forest",
    **kwargs
) -> IAnomalyDetector:
    """
    Factory to create anomaly detectors.
    
    Args:
        detector_type: 'isolation_forest' or 'lof'
        **kwargs: Additional parameters for the detector
    
    Returns:
        IAnomalyDetector instance
    """
    if detector_type == "isolation_forest":
        return IsolationForestDetector(**kwargs)
    elif detector_type == "lof":
        return LocalOutlierFactorDetector(**kwargs)
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")