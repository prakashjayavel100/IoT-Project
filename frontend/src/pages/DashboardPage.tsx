import { useEffect, useState } from 'react'
import { DashboardSummary, DashboardDeviceItem, getDashboardSummary, getDashboardDevices, apiErrorMessage } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [devices, setDevices] = useState<DashboardDeviceItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    Promise.all([getDashboardSummary(), getDashboardDevices()])
      .then(([summaryData, deviceData]) => {
        setSummary(summaryData)
        setDevices(deviceData)
      })
      .catch((err) => setError(apiErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  if (error) {
    return <ErrorBanner message={error} />
  }

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h1>Security posture overview</h1>
        </div>
      </div>

      {summary ? (
        <div className="grid grid-4">
          <div className="card"> <span className="label">Total devices</span> <strong>{summary.total_devices}</strong> </div>
          <div className="card"> <span className="label">Trusted devices</span> <strong>{summary.trusted_devices}</strong> </div>
          <div className="card"> <span className="label">Anomalous devices</span> <strong>{summary.anomaly_devices}</strong> </div>
          <div className="card"> <span className="label">Drift detected</span> <strong>{summary.drift_devices}</strong> </div>
        </div>
      ) : (
        <div className="empty-state">No dashboard summary available.</div>
      )}

      <section className="section-card">
        <div className="section-header">
          <div>
            <h2>Device security overview</h2>
            <p>Latest trust status for registered devices.</p>
          </div>
        </div>

        {devices.length ? (
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Device</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Trust score</th>
                  <th>Last activity</th>
                </tr>
              </thead>
              <tbody>
                {devices.map((device) => (
                  <tr key={device.device_id}>
                    <td>{device.device_name}</td>
                    <td>{device.device_type}</td>
                    <td><span className={`badge badge-${device.latest_status?.toLowerCase() ?? 'unknown'}`}>{device.latest_status ?? 'Unknown'}</span></td>
                    <td>{device.latest_trust_score?.toFixed(2) ?? '—'}</td>
                    <td>{device.latest_timestamp ? new Date(device.latest_timestamp).toLocaleString() : '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No devices found for dashboard.</div>
        )}
      </section>
    </div>
  )
}
