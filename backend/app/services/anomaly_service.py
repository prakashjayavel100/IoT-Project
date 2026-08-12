from sklearn.ensemble import IsolationForest
from typing import List, Optional, Dict, Any


def _validate_features(features: List[float]) -> List[float]:
    if not isinstance(features, list):
        raise ValueError("Features must be provided as a list of numeric values")
    if len(features) != 4:
        raise ValueError("Exactly 4 features are required: packet_rate, behavior_score, network_score, firmware_score")
    for value in features:
        if not isinstance(value, (int, float)):
            raise ValueError("All feature values must be numeric")
    return [float(value) for value in features]


def build_isolation_forest(feature_matrix: List[List[float]], contamination: float = 0.1) -> IsolationForest:
    """Train an Isolation Forest model on a matrix of feature rows.

    Isolation Forest is an unsupervised algorithm that isolates anomalies
    by building random decision trees. Points that are easier to isolate
    (require fewer splits) are more likely to be anomalous.
    """
    if not isinstance(feature_matrix, list) or not feature_matrix:
        raise ValueError("feature_matrix must be a non-empty list of feature rows")
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(feature_matrix)
    return model


_default_model: Optional[IsolationForest] = None


def get_default_isolation_forest() -> IsolationForest:
    """Return a default Isolation Forest model trained on example normal behavior."""
    global _default_model
    if _default_model is None:
        normal_samples = [
            [10.0, 85.0, 90.0, 95.0],
            [12.0, 80.0, 88.0, 92.0],
            [8.0, 88.0, 92.0, 96.0],
            [15.0, 82.0, 85.0, 90.0],
            [7.0, 90.0, 94.0, 98.0],
            [9.0, 87.0, 91.0, 94.0],
        ]
        _default_model = build_isolation_forest(normal_samples, contamination=0.1)
    return _default_model


def detect_anomaly(features: List[float], model: Optional[IsolationForest] = None) -> Dict[str, Any]:
    """Detect whether a feature vector is anomalous using Isolation Forest.

    Returns a dictionary with boolean anomaly detection, anomaly score,
    and raw prediction label (1 = normal, -1 = anomaly).
    """
    validated = _validate_features(features)
    if model is None:
        raise ValueError("A trained IsolationForest model must be provided")

    prediction = int(model.predict([validated])[0])
    score = float(model.decision_function([validated])[0])
    anomaly_detected = prediction == -1

    return {
        "anomaly_detected": anomaly_detected,
        "anomaly_score": score,
        "prediction": prediction,
    }


def explain_isolation_forest() -> str:
    """Return a short explanation for documentation or teaching."""
    return (
        "Isolation Forest detects anomalies by randomly partitioning feature space "
        "and identifying points that are isolated by fewer splits. It is suitable "
        "for IoT behavior because abnormal device states are often rare and "
        "different from normal patterns. The anomaly score measures how far the "
        "sample is from the normal region: lower scores mean more anomalous."
    )
