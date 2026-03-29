# Machine Learning Fundamentals

## What is Machine Learning?

Machine Learning (ML) is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.

## Types of Machine Learning

### 1. Supervised Learning
The model learns from labeled data.
- Classification: Predicting categorical labels
- Regression: Predicting continuous values

### 2. Unsupervised Learning
The model learns from unlabeled data.
- Clustering: Grouping similar data points
- Dimensionality Reduction: Reducing feature space

### 3. Reinforcement Learning
The model learns through trial and error with rewards.

## Popular Algorithms

| Algorithm | Type | Use Case |
|-----------|------|----------|
| Linear Regression | Supervised | Prediction |
| Decision Trees | Supervised | Classification |
| K-Means | Unsupervised | Clustering |
| Random Forest | Supervised | Classification/Regression |
| SVM | Supervised | Classification |

## Evaluation Metrics

- **Accuracy**: Correct predictions / Total predictions
- **Precision**: True Positives / (True Positives + False Positives)
- **Recall**: True Positives / (True Positives + False Negatives)
- **F1-Score**: Harmonic mean of Precision and Recall

## Example: Training a Model

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2
)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy}")
```

## Deep Learning

Deep Learning uses neural networks with multiple layers (deep neural networks). It excels at:
- Image recognition
- Natural Language Processing
- Speech recognition

## Conclusion

Machine Learning is transforming industries and enabling new applications across healthcare, finance, and technology.