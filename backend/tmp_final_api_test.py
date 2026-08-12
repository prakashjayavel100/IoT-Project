import urllib.request
import urllib.error
import json

BASE_URL = 'http://127.0.0.1:8003'

def request(method, path, data=None):
    url = BASE_URL + path
    body = None
    headers = {}
    if data is not None:
        body = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read().decode('utf-8'))
        except Exception:
            return exc.code, exc.read().decode('utf-8')
    except Exception as exc:
        return None, {'error': str(exc)}

print('HEALTH', request('GET', '/health'))
print('HEALTH DB', request('GET', '/health/database'))
print('REGISTER', request('POST', '/api/devices', {'device_id':'CAM001','device_name':'Smart Camera 01','device_type':'smart_camera'}))
print('DUPLICATE', request('POST', '/api/devices', {'device_id':'CAM001','device_name':'Smart Camera 01','device_type':'smart_camera'}))
print('LIST', request('GET', '/api/devices'))
print('GET CAM001', request('GET', '/api/devices/CAM001'))
print('GET UNKNOWN', request('GET', '/api/devices/UNKNOWN'))
print('RAW DATA', request('POST', '/api/devices/CAM001/data', {'packet_rate':500,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('ANALYZE', request('POST', '/api/devices/CAM001/analyze', {'packet_rate':500,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('INVALID_ANALYZE_NEG', request('POST', '/api/devices/CAM001/analyze', {'packet_rate':-10,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('INVALID_ANALYZE_HIGH', request('POST', '/api/devices/CAM001/analyze', {'packet_rate':10,'behavior_score':150,'network_score':92,'firmware_score':95}))
print('INVALID_ANALYZE_STRING', request('POST', '/api/devices/CAM001/analyze', {'packet_rate':10,'behavior_score':90,'network_score':92,'firmware_score':'abc'}))
print('INVALID_ANALYZE_MISSING', request('POST', '/api/devices/CAM001/analyze', {'packet_rate':10,'behavior_score':90,'network_score':92}))
print('UNKNOWN_DEVICE_ANALYZE', request('POST', '/api/devices/UNKNOWN/analyze', {'packet_rate':10,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('DASHBOARD_SUMMARY', request('GET', '/api/dashboard/summary'))
print('DASHBOARD_DEVICES', request('GET', '/api/dashboard/devices'))
print('DEVICE_HISTORY', request('GET', '/api/dashboard/devices/CAM001/history'))
print('NOTIFICATIONS', request('GET', '/api/notifications'))
print('NOTIFICATIONS_DEVICE', request('GET', '/api/notifications/CAM001'))
