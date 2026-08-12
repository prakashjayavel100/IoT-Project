import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getDeviceById, getDeviceHistory, apiErrorMessage } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'

export default function DeviceDetailsPage() {
  const { deviceId } = useParams()
  const [device, setDevice] = useState<any | null>(null)
  const [history, setHistory] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const id = deviceId || ''
    if (!id) return

    setLoading(true)
    Promise.all([getDeviceById(id), getDeviceHistory(id)])
      .then(([deviceData, historyData]) => {
        setDevice(deviceData)
        setHistory(historyData)
      })
      .catch((err) => setError(apiErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [deviceId])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorBanner message={error} />
  if (!device) return <div className="empty-state">Device not found.</div>

  return (
    <div className="page-content">
      <div className="page-header">
        <p className="eyebrow">Device details</p>
        <h1>{device.device_name}</h1>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h2>Device profile</h2>
          <dl>
            <dt>Device ID</dt>
            <dd>{device.device_id}</dd>
            <dt>Type</dt>
            <dd>{device.device_type}</dd>
            <dt>Registered</dt>
            <dd>{device.created_at ? new Date(device.created_at).toLocaleString() : 'Unknown'}</dd>
          </dl>
        </div>
      </div>

      <section className="section-card">
        <div className="section-header">
          <div>
            <h2>Recent analysis history</h2>
            <p>Latest trust and security events for this device.</p>
          </div>
        </div>

        {history.length ? (
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Status</th>
                  <th>Trust</th>
                  <th>Anomaly</th>
                  <th>Drift</th>
                </tr>
              </thead>
              <tbody>
                {history.map((entry, index) => (
                  <tr key={index}>
                    <td>{new Date(entry.timestamp).toLocaleString()}</td>
                    <td><span className={`badge badge-${entry.status.toLowerCase()}`}>{entry.status}</span></td>
                    <td>{entry.trust_score.toFixed(2)}</td>
                    <td>{entry.anomaly_detected ? 'Yes' : 'No'}</td>
                    <td>{entry.drift_detected ? 'Yes' : 'No'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No analysis history available for this device.</div>
        )}
      </section>
    </div>
  )
}
