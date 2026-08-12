import { useEffect, useState } from 'react'
import { Route, Routes, Navigate } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import DashboardPage from './pages/DashboardPage'
import DevicesPage from './pages/DevicesPage'
import AnalysisPage from './pages/AnalysisPage'
import NotificationsPage from './pages/NotificationsPage'
import DeviceDetailsPage from './pages/DeviceDetailsPage'
import SettingsPage from './pages/SettingsPage'
import { getHealthStatus } from './services/api'

function App() {
  const [apiStatus, setApiStatus] = useState<'ok' | 'unavailable'>('unavailable')

  useEffect(() => {
    getHealthStatus()
      .then(() => setApiStatus('ok'))
      .catch(() => setApiStatus('unavailable'))
  }, [])

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <Topbar apiStatus={apiStatus} />
        <div className="page-frame">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/devices" element={<DevicesPage />} />
            <Route path="/devices/:deviceId" element={<DeviceDetailsPage />} />
            <Route path="/analysis" element={<AnalysisPage />} />
            <Route path="/notifications" element={<NotificationsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<div className="empty-state">Page not found</div>} />
          </Routes>
        </div>
      </div>
    </div>
  )
}

export default App
