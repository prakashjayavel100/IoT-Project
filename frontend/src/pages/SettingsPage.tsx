export default function SettingsPage() {
  return (
    <div className="page-content">
      <div className="page-header">
        <p className="eyebrow">Settings</p>
        <h1>Application settings</h1>
      </div>
      <div className="empty-state">
        Configuration is handled by the backend and environment variables. No user settings are supported yet.
      </div>
    </div>
  )
}
