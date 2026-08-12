from typing import Dict, List, Union


def extract_features(device_data: Dict[str, Union[int, float]]) -> List[float]:
    """Convert raw device input into a numerical feature vector.

    Feature extraction prepares the input values for use by machine learning models,
    like scikit-learn's Isolation Forest. This keeps the route logic separate from
    ML preprocessing and makes the model input easier to validate and test.
    """

    required_fields = [
        "packet_rate",
        "behavior_score",
        "network_score",
        "firmware_score",
    ]

    features = []
    for field in required_fields:
        if field not in device_data:
            raise ValueError(f"Missing required feature: {field}")

        value = device_data[field]
        if not isinstance(value, (int, float)):
            raise ValueError(f"Feature '{field}' must be numeric")

        features.append(float(value))

    return features
