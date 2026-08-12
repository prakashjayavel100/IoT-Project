import { NavLink } from 'react-router-dom'

const links = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Devices', path: '/devices' },
  { label: 'Analysis', path: '/analysis' },
  { label: 'Notifications', path: '/notifications' },
  { label: 'Settings', path: '/settings' },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">IoT Trust Drift</div>
      <nav className="sidebar-nav">
        {links.map((link) => (
          <NavLink key={link.path} to={link.path} className={({ isActive }) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
