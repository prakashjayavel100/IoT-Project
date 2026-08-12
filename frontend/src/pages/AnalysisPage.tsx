import { FormEvent, useEffect, useState } from 'react'
import { analyzeDevice, apiErrorMessage, AnalysisResult, DeviceInDB, listDevices } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'

export default function AnalysisPage() {
  const [devices, setDevices] = useState<DeviceInDB[]>([])
  const [selectedDeviceId, setSelectedDeviceId] = useState('')
  const [manualDeviceId, setManualDeviceId] = useState('')
  const [packetRate, setPacketRate] = useState('')
  const [behaviorScore, setBehaviorScore] = useState('')
  const [networkScore, setNetworkScore] = useState('')
  const [firmwareScore, setFirmwareScore] = useState('')
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listDevices()
      .then((devices) => {
        setDevices(devices)
        if (devices.length > 0) {
          setSelectedDeviceId(devices[0].device_id)
        }
      })
      .catch((err) => {
        setError(apiErrorMessage(err))
      })
  }, [])

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    setResult(null)
    setLoading(true)

    const deviceId = manualDeviceId.trim() || selectedDeviceId
    if (!deviceId) {
      setError('Please select or enter a valid device ID.')
      setLoading(false)
      return
    }

    try {
      const data = await analyzeDevice(deviceId, {
        packet_rate: Number(packetRate),
        behavior_score: Number(behaviorScore),
        network_score: Number(networkScore),
        firmware_score: Number(firmwareScore),
      })
      setResult(data)
    } catch (err) {
      setError(apiErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-content">
      <div className="page-header">
        <p className="eyebrow">Analysis</p>
        <h1>Run real device analysis</h1>
      </div>

      <form className="form-panel" onSubmit={handleSubmit}>
        <label>
          Select device
          <select value={selectedDeviceId} onChange={(event) => setSelectedDeviceId(event.target.value)}>
            <option value="" disabled>
              Choose a registered device
            </option>
            {devices.map((device) => (
              <option key={device.device_id} value={device.device_id}>
                {device.device_name} ({device.device_id})
              </option>
            ))}
          </select>
        </label>

        <label>
          Or enter device ID
          <input
            value={manualDeviceId}
            onChange={(event) => setManualDeviceId(event.target.value)}
            placeholder="device-123"
          />
        </label>

        <label>
          Packet rate
          <input type="number" value={packetRate} onChange={(event) => setPacketRate(event.target.value)} required />
        </label>

        <label>
          Behavior score
          <input type="number" value={behaviorScore} onChange={(event) => setBehaviorScore(event.target.value)} required />
        </label>

        <label>
          Network score
          <input type="number" value={networkScore} onChange={(event) => setNetworkScore(event.target.value)} required />
        </label>

        <label>
          Firmware score
          <input type="number" value={firmwareScore} onChange={(event) => setFirmwareScore(event.target.value)} required />
        </label>

        <button className="button button-primary" type="submit" disabled={loading}>
          {loading ? 'Analyzing…' : 'Analyze Device'}
        </button>
      </form>

      {error && <ErrorBanner message={error} />}

      {result && (
        <div className="analysis-result-card">
          <h2>Analysis result</h2>
          <div className="status-row">
            <div>
              <span className="label">Status</span>
              <div className={`badge badge-${result.status.toLowerCase()}`}>{result.status}</div>
            </div>
            <div>
              <span className="label">Trust score</span>
              <div className="trust-score">{result.trust_score.toFixed(2)}</div>
            </div>
          </div>

          <div className="grid grid-4">
            <div className="card small-card">
              <span className="label">Anomaly</span>
              <strong>{result.anomaly_detected ? 'Detected' : 'Not detected'}</strong>
            </div>
            <div className="card small-card">
              <span className="label">Drift</span>
              <strong>{result.drift_detected ? 'Detected' : 'Stable'}</strong>
            </div>
            <div className="card small-card">
              <span className="label">Anomaly score</span>
              <strong>{result.anomaly_score.toFixed(4)}</strong>
            </div>
            <div className="card small-card">
              <span className="label">Timestamp</span>
              <strong>{new Date(result.timestamp).toLocaleString()}</strong>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
