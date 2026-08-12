from typing import Dict


def compute_trust_score(device_data: Dict[str, float]) -> Dict[str, object]:
    """Compute a deterministic trust score from device behavior inputs.

    The score is based on device health measures and anomaly/drift signals.
    Higher values mean the device is more trustworthy.
    """
    # Normalized base score from device metrics: behavior, network, firmware.
    # Each metric is expected to be between 0 and 100.
    behavior = float(device_data.get("behavior_score", 0))
    network = float(device_data.get("network_score", 0))
    firmware = float(device_data.get("firmware_score", 0))

    # Start with the average of the main quality scores.
    base_score = (behavior + network + firmware) / 3.0

    # Subtract penalties from anomaly and drift.
    # A stronger anomaly detection (more negative anomaly_score) reduces trust more.
    anomaly_detected = bool(device_data.get("anomaly_detected", False))
    drift_detected = bool(device_data.get("drift_detected", False))
    anomaly_score = float(device_data.get("anomaly_score", 0))

    # Convert anomaly score into a penalty.
    # Isolation Forest scores are higher for normal points and lower for anomalies.
    # We use a simple mapping: normal values near 0 still have small penalty, anomalies are penalized more.
    anomaly_penalty = 0.0
    if anomaly_detected:
        anomaly_penalty = min(30.0, abs(anomaly_score) * 10)
    else:
        anomaly_penalty = max(0.0, 5.0 - abs(anomaly_score))

    # Drift is treated as the highest risk, with a strong fixed penalty.
    drift_penalty = 40.0 if drift_detected else 0.0

    # Combine base score and penalties.
    trust_score = base_score - anomaly_penalty - drift_penalty

    # Clamp score between 0 and 100.
    trust_score = max(0.0, min(100.0, trust_score))

    # Determine status with priority: DRIFT > ANOMALY > TRUSTED
    if drift_detected:
        status = "DRIFT"
    elif anomaly_detected:
        status = "ANOMALY"
    else:
        status = "TRUSTED"

    return {"trust_score": trust_score, "status": status}
