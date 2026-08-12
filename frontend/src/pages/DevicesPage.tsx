import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { listDevices, apiErrorMessage } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'

export default function DevicesPage() {
  const [devices, setDevices] = useState<any[]>([])
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    listDevices()
      .then((data) => setDevices(data))
      .catch((err) => setError(apiErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [])

  const filtered = useMemo(() => {
    const lower = query.toLowerCase()
    return devices.filter((device) =>
      device.device_id.toLowerCase().includes(lower) ||
      device.device_name.toLowerCase().includes(lower) ||
      device.device_type.toLowerCase().includes(lower),
    )
  }, [devices, query])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorBanner message={error} />

  return (
    <div className="page-content">
      <div className="page-header page-header-split">
        <div>
          <p className="eyebrow">Devices</p>
          <h1>Registered devices</h1>
        </div>
        <input
          className="search-input"
          placeholder="Search devices..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </div>

      {filtered.length ? (
        <div className="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Device ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Registered</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((device) => (
                <tr key={device.device_id}>
                  <td>{device.device_id}</td>
                  <td>{device.device_name}</td>
                  <td>{device.device_type}</td>
                  <td>{device.created_at ? new Date(device.created_at).toLocaleString() : '—'}</td>
                  <td><Link className="button button-small" to={`/devices/${device.device_id}`}>View</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">No devices are registered yet.</div>
      )}
    </div>
  )
}
