import { useEffect, useState } from 'react'
import { listNotifications, apiErrorMessage } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadNotifications = () => {
    setError(null)
    setLoading(true)
    listNotifications()
      .then((data) => setNotifications(data))
      .catch((err) => setError(apiErrorMessage(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadNotifications()
  }, [])

  return (
    <div className="page-content">
      <div className="page-header page-header-split">
        <div>
          <p className="eyebrow">Notifications</p>
          <h1>Security alerts</h1>
        </div>
        <button className="button button-secondary" onClick={loadNotifications}>Refresh</button>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorBanner message={error} />}

      {!loading && !error && (
        <div>
          {notifications.length ? (
            <div className="table-responsive">
              <table>
                <thead>
                  <tr>
                    <th>Device</th>
                    <th>Status</th>
                    <th>Message</th>
                    <th>Trust score</th>
                    <th>When</th>
                  </tr>
                </thead>
                <tbody>
                  {notifications.map((item, index) => (
                    <tr key={`${item.device_id}-${index}`}>
                      <td>{item.device_id}</td>
                      <td><span className={`badge badge-${item.status.toLowerCase()}`}>{item.status}</span></td>
                      <td>{item.message}</td>
                      <td>{item.trust_score?.toFixed(2)}</td>
                      <td>{new Date(item.timestamp).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="empty-state">No notifications are available.</div>
          )}
        </div>
      )}
    </div>
  )
}
