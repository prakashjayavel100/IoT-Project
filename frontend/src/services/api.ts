import axios from 'axios'
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'https://iot-trust-backend.onrender.com'

console.log("API BASE URL:", API_BASE_URL)

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

export interface DeviceRegisterPayload {
  device_id: string
  device_name: string
  device_type: string
}

export interface DeviceDataPayload {
  packet_rate: number
  behavior_score: number
  network_score: number
  firmware_score: number
}

export interface DeviceInDB {
  device_id: string
  device_name: string
  device_type: string
  created_at?: string
}

export interface AnalysisResult {
  device_id: string
  input_features: Record<string, number>
  anomaly_detected: boolean
  anomaly_score: number
  drift_detected: boolean
  trust_score: number
  status: string
  timestamp: string
}

export interface DashboardSummary {
  total_devices: number
  trusted_devices: number
  anomaly_devices: number
  drift_devices: number
  total_analysis_today: number
  critical_devices: number
}

export interface DashboardDeviceItem {
  device_id: string
  device_name: string
  device_type: string
  latest_trust_score?: number
  latest_status?: string
  latest_anomaly_result?: boolean
  latest_drift_result?: boolean
  latest_timestamp?: string
}

export interface NotificationItem {
  device_id: string
  status: string
  event_type: string
  description: string
  trust_score: number
  level: string
  message: string
  timestamp: string
}

export type HealthStatus = { status: string }

export const getHealthStatus = async () => {
  const response = await api.get<HealthStatus>('/health')
  return response.data
}

export const getHealthDatabaseStatus = async () => {
  const response = await api.get<{ database: string }>('/health/database')
  return response.data
}

export const listDevices = async () => {
  const response = await api.get<DeviceInDB[]>('/api/devices')
  return response.data
}

export const getDeviceById = async (deviceId: string) => {
  const response = await api.get<DeviceInDB>(`/api/devices/${deviceId}`)
  return response.data
}

export const registerDevice = async (payload: DeviceRegisterPayload) => {
  const response = await api.post('/api/devices', payload)
  return response.data
}

export const analyzeDevice = async (deviceId: string, payload: DeviceDataPayload) => {
  const response = await api.post<AnalysisResult>(`/api/devices/${deviceId}/analyze`, payload)
  return response.data
}

export const getDashboardSummary = async () => {
  const response = await api.get<DashboardSummary>('/api/dashboard/summary')
  return response.data
}

export const getDashboardDevices = async () => {
  const response = await api.get<DashboardDeviceItem[]>('/api/dashboard/devices')
  return response.data
}

export const getDeviceHistory = async (deviceId: string) => {
  const response = await api.get<AnalysisResult[]>(`/api/dashboard/devices/${deviceId}/history`)
  return response.data
}

export const listNotifications = async () => {
  const response = await api.get<NotificationItem[]>('/api/notifications')
  return response.data
}

export const listNotificationsForDevice = async (deviceId: string) => {
  const response = await api.get<NotificationItem[]>(`/api/notifications/${deviceId}`)
  return response.data
}

export const apiErrorMessage = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      return error.response.data?.message || `Request failed with status ${error.response.status}`
    }
    if (error.request) {
      return 'Unable to connect to backend. Please check that the server is running.'
    }
    return error.message
  }
  return 'An unexpected error occurred.'
}
