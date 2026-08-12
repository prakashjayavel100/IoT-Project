import pytest

from app.services import anomaly_service, drift_service, feature_service, trust_service


def test_feature_extraction_happy_path():
    device_data = {
        "packet_rate": 10,
        "behavior_score": 80,
        "network_score": 90,
        "firmware_score": 95,
    }
    features = feature_service.extract_features(device_data)
    assert features == [10.0, 80.0, 90.0, 95.0]


def test_feature_extraction_missing_field():
    with pytest.raises(ValueError, match="Missing required feature: packet_rate"):
        feature_service.extract_features({"behavior_score": 80, "network_score": 90, "firmware_score": 95})


def test_isolation_forest_anomaly_detection():
    normal_samples = [
        [10.0, 85.0, 90.0, 95.0],
        [12.0, 82.0, 88.0, 92.0],
        [11.0, 80.0, 89.0, 93.0],
        [13.0, 83.0, 91.0, 94.0],
    ]
    model = anomaly_service.build_isolation_forest(normal_samples, contamination=0.1)

    normal_features = [11.0, 84.0, 89.0, 94.0]
    normal_result = anomaly_service.detect_anomaly(normal_features, model)
    assert normal_result["anomaly_detected"] is False
    assert normal_result["prediction"] == 1

    anomaly_features = [100.0, 0.0, 0.0, 0.0]
    anomaly_result = anomaly_service.detect_anomaly(anomaly_features, model)
    assert anomaly_result["anomaly_detected"] is True
    assert anomaly_result["prediction"] == -1


def test_adwin_drift_detection_sequence():
    device_id = "drift-device"
    # Use a stable baseline first; ADWIN should not trigger immediately.
    for value in [100.0, 102.0, 99.0, 101.0, 100.5]:
        result = drift_service.detect_drift(device_id, {
            "packet_rate": value,
            "behavior_score": 80.0,
            "network_score": 90.0,
            "firmware_score": 95.0,
        })
        assert result["drift_detected"] is False

    # Introduce a strong shift to trigger drift on a deterministic stream.
    drift_result = drift_service.detect_drift(device_id, {
        "packet_rate": 500.0,
        "behavior_score": 10.0,
        "network_score": 10.0,
        "firmware_score": 10.0,
    })
    assert drift_result["drift_detected"] is True


def test_trust_score_calculation():
    result = trust_service.compute_trust_score({
        "behavior_score": 80,
        "network_score": 90,
        "firmware_score": 95,
        "anomaly_detected": False,
        "anomaly_score": 0.2,
        "drift_detected": False,
    })
    assert pytest.approx(result["trust_score"], rel=1e-3) == (80 + 90 + 95) / 3.0 - max(0.0, 5.0 - abs(0.2))
    assert result["status"] == "TRUSTED"

    anomaly_result = trust_service.compute_trust_score({
        "behavior_score": 80,
        "network_score": 90,
        "firmware_score": 95,
        "anomaly_detected": True,
        "anomaly_score": -2.0,
        "drift_detected": False,
    })
    assert anomaly_result["status"] == "ANOMALY"

    drift_result = trust_service.compute_trust_score({
        "behavior_score": 80,
        "network_score": 90,
        "firmware_score": 95,
        "anomaly_detected": True,
        "anomaly_score": -2.0,
        "drift_detected": True,
    })
    assert drift_result["status"] == "DRIFT"
