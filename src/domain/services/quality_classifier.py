"""
Quality classification module for technical documents.

Uses supervised learning to classify documents by quality
based on features extracted from embeddings.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from numpy.typing import NDArray
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

logger = logging.getLogger(__name__)


class QualityLabel:
    """Quality label enumeration"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
    @classmethod
    def all(cls) -> List[str]:
        return [cls.HIGH, cls.MEDIUM, cls.LOW]


class IQualityClassifier(ABC):
    """Interface for quality classifiers"""
    
    @abstractmethod
    def fit(
        self, 
        embeddings: NDArray[np.float32], 
        labels: List[str]
    ) -> None:
        """Train the classifier"""
        pass
    
    @abstractmethod
    def predict(self, embedding: NDArray[np.float32]) -> str:
        """Predict the quality of a document"""
        pass
    
    @abstractmethod
    def predict_batch(self, embeddings: NDArray[np.float32]) -> List[str]:
        """Predict the quality of multiple documents"""
        pass
    
    @abstractmethod
    def get_confidence(self, embedding: NDArray[np.float32]) -> Dict[str, float]:
        """Return probabilities for each class"""
        pass


class QualityClassifier(IQualityClassifier):
    """
    Quality classifier based on Random Forest.
    
    This classifier categorizes documents into three quality levels:
    - high: Well-structured and relevant documents
    - medium: Moderate quality documents
    - low: Low quality or non-relevant documents
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        random_state: int = 42
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self._model: Optional[RandomForestClassifier] = None
        self._scaler: Optional[StandardScaler] = None
        self._is_fitted = False
        self._classes: Optional[List[str]] = None
        
    def fit(
        self, 
        embeddings: NDArray[np.float32], 
        labels: List[str]
    ) -> None:
        """Train the classifier with embeddings and labels"""
        try:
            # Scale embeddings
            self._scaler = StandardScaler()
            embeddings_scaled = self._scaler.fit_transform(embeddings)
            
            # Train model
            self._model = RandomForestClassifier(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                random_state=self.random_state,
                n_jobs=-1,
                class_weight="balanced"  # Handle class imbalance
            )
            self._model.fit(embeddings_scaled, labels)
            
            self._classes = self._model.classes_.tolist()
            self._is_fitted = True
            logger.info(f"Quality classifier trained with {len(labels)} samples")
            
        except Exception as e:
            logger.error(f"Error training quality classifier: {str(e)}")
            raise
    
    def predict(self, embedding: NDArray[np.float32]) -> str:
        """Predict the quality of a document"""
        if not self._is_fitted:
            raise ValueError("Classifier has not been trained yet")
        
        embedding_scaled = self._scaler.transform(embedding.reshape(1, -1))
        prediction = self._model.predict(embedding_scaled)
        return str(prediction[0])
    
    def predict_batch(self, embeddings: NDArray[np.float32]) -> List[str]:
        """Predict the quality of multiple documents"""
        if not self._is_fitted:
            raise ValueError("Classifier has not been trained yet")
        
        embeddings_scaled = self._scaler.transform(embeddings)
        predictions = self._model.predict(embeddings_scaled)
        return predictions.tolist()
    
    def get_confidence(self, embedding: NDArray[np.float32]) -> Dict[str, float]:
        """Return probabilities for each class"""
        if not self._is_fitted:
            raise ValueError("Classifier has not been trained yet")
        
        embedding_scaled = self._scaler.transform(embedding.reshape(1, -1))
        probabilities = self._model.predict_proba(embedding_scaled)[0]
        
        return {
            str(cls): float(prob)
            for cls, prob in zip(self._model.classes_, probabilities)
        }
    
    def get_feature_importance(self) -> Optional[NDArray[np.float32]]:
        """Return feature (embedding) importance"""
        if not self._is_fitted:
            return None
        return self._model.feature_importances_


class GradientBoostingQualityClassifier(IQualityClassifier):
    """
    Quality classifier using Gradient Boosting.
    
    More accurate but slower alternative to Random Forest.
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        random_state: int = 42
    ) -> None:
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state
        self._model: Optional[GradientBoostingClassifier] = None
        self._scaler: Optional[StandardScaler] = None
        self._is_fitted = False
        self._classes: Optional[List[str]] = None
        
    def fit(
        self, 
        embeddings: NDArray[np.float32], 
        labels: List[str]
    ) -> None:
        try:
            self._scaler = StandardScaler()
            embeddings_scaled = self._scaler.fit_transform(embeddings)
            
            self._model = GradientBoostingClassifier(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=self.max_depth,
                random_state=self.random_state
            )
            self._model.fit(embeddings_scaled, labels)
            
            self._classes = self._model.classes_.tolist()
            self._is_fitted = True
            logger.info(f"Gradient Boosting trained with {len(labels)} samples")
        except Exception as e:
            logger.error(f"Error training Gradient Boosting: {str(e)}")
            raise
    
    def predict(self, embedding: NDArray[np.float32]) -> str:
        if not self._is_fitted:
            raise ValueError("Classifier has not been trained yet")
        
        embedding_scaled = self._scaler.transform(embedding.reshape(1, -1))
        return str(self._model.predict(embedding_scaled)[0])
    
    def predict_batch(self, embeddings: NDArray[np.float32]) -> List[str]:
        if not self._is_fitted:
            raise ValueError("Classifier has not been trained yet")
        
        embeddings_scaled = self._scaler.transform(embeddings)
        return self._model.predict(embeddings_scaled).tolist()
    
    def get_confidence(self, embedding: NDArray[np.float32]) -> Dict[str, float]:
        if not self._is_fitted:
            raise ValueError("Classifier has not been trained yet")
        
        embedding_scaled = self._scaler.transform(embedding.reshape(1, -1))
        probabilities = self._model.predict_proba(embedding_scaled)[0]
        
        return {
            str(cls): float(prob)
            for cls, prob in zip(self._model.classes_, probabilities)
        }


def create_quality_classifier(
    classifier_type: str = "random_forest",
    **kwargs
) -> IQualityClassifier:
    """
    Factory to create quality classifiers.
    
    Args:
        classifier_type: 'random_forest' or 'gradient_boosting'
        **kwargs: Additional parameters
    
    Returns:
        IQualityClassifier instance
    """
    if classifier_type == "random_forest":
        return QualityClassifier(**kwargs)
    elif classifier_type == "gradient_boosting":
        return GradientBoostingQualityClassifier(**kwargs)
    else:
        raise ValueError(f"Unknown classifier type: {classifier_type}")


class QualityAssessmentService:
    """
    Quality assessment service that combines multiple metrics.
    """
    
    def __init__(self, classifier: IQualityClassifier) -> None:
        self.classifier = classifier
        
    def assess_document(
        self, 
        embedding: NDArray[np.float32]
    ) -> Dict[str, Any]:
        """
        Assess the quality of a document
        Return dictionary with quality and confidence
        """
        quality = self.classifier.predict(embedding)
        confidence = self.classifier.get_confidence(embedding)
        
        return {
            "quality": quality,
            "confidence": confidence,
            "is_high_quality": quality == QualityLabel.HIGH
        }
    
    def assess_batch(
        self, 
        embeddings: NDArray[np.float32]
    ) -> List[Dict[str, Any]]:
        """Assess the quality of multiple documents"""
        qualities = self.classifier.predict_batch(embeddings)
        
        results = []
        for i, quality in enumerate(qualities):
            embedding = embeddings[i:i+1]
            confidence = self.classifier.get_confidence(embedding[0])
            
            results.append({
                "quality": quality,
                "confidence": confidence,
                "is_high_quality": quality == QualityLabel.HIGH
            })
        
        return results