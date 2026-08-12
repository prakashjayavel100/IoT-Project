interface TopbarProps {
  apiStatus: 'ok' | 'unavailable'
}

export default function Topbar({ apiStatus }: TopbarProps) {
  return (
    <header className="topbar">
      <div className="topbar-title">IoT Trust Drift Detection</div>
      <div className="topbar-actions">
        <div className={`status-pill ${apiStatus === 'ok' ? 'status-ok' : 'status-error'}`}>
          {apiStatus === 'ok' ? 'Backend Connected' : 'Backend Offline'}
        </div>
      </div>
    </header>
  )
}
