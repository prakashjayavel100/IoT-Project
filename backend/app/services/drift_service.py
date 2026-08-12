from typing import Dict, Optional

from river.drift import ADWIN


class DeviceDriftState:
    """Maintain ADWIN state for a single device."""

    def __init__(self):
        self.detector = ADWIN(grace_period=1, min_window_length=5, delta=0.01)
        self.values: list[float] = []
        self.initialized = False

    def update(self, value: float) -> bool:
        """Update the ADWIN detector with a new value and return whether drift is detected."""
        self.detector.update(value)
        self.values.append(value)
        self.initialized = True

        if hasattr(self.detector, "change_detected"):
            drift_detected = bool(getattr(self.detector, "change_detected"))
        elif hasattr(self.detector, "change"):
            drift_detected = bool(getattr(self.detector, "change"))
        elif hasattr(self.detector, "drift_detected"):
            drift_detected = bool(getattr(self.detector, "drift_detected"))
        else:
            drift_detected = False

        if not drift_detected and len(self.values) >= 5:
            recent_mean = sum(self.values[-5:]) / 5.0
            if abs(value - recent_mean) > 50.0:
                drift_detected = True

        return drift_detected


# Store a detector per device_id so each device stream is independent.
_device_detectors: Dict[str, DeviceDriftState] = {}


def _get_device_state(device_id: str) -> DeviceDriftState:
    if device_id not in _device_detectors:
        _device_detectors[device_id] = DeviceDriftState()
    return _device_detectors[device_id]


def compute_behavior_metric(device_data: Dict[str, float]) -> float:
    """Compute a simple numeric behavior metric from device input.

    This can be used as the sequential stream for ADWIN. A normalized
    sum of the IoT feature values is easy to explain and highlights
    changes in overall device behavior.
    """
    return (
        float(device_data['packet_rate'])
        + float(device_data['behavior_score'])
        + float(device_data['network_score'])
        + float(device_data['firmware_score'])
    )


def detect_drift(device_id: str, device_data: Dict[str, float]) -> Dict[str, object]:
    """Detect concept drift for a single device using ADWIN.

    Returns a dict with drift detection result and the current behavior metric.
    """
    if any(key not in device_data for key in ['packet_rate', 'behavior_score', 'network_score', 'firmware_score']):
        raise ValueError('Missing required device data values for drift detection')

    value = compute_behavior_metric(device_data)
    state = _get_device_state(device_id)
    drift_detected = state.update(value)

    return {
        'device_id': device_id,
        'drift_detected': bool(drift_detected),
        'current_value': value,
    }


def explain_drift() -> str:
    return (
        'Concept drift means that the statistical behavior of a device stream changes over time. '
        'ADWIN watches a sequence of values and automatically detects when the recent behavior '
        'differs enough from the past. Each device keeps its own detector so one device changing '
        'does not affect the drift assessment of others.'
    )
