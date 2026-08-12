import urllib.request
import urllib.error
import json

BASE_URL = 'http://127.0.0.1:8001'

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
        return exc.code, json.loads(exc.read().decode('utf-8'))
    except Exception as exc:
        return None, {'error': str(exc)}

# Register device
payload = {
    'device_id': 'CAM001',
    'device_name': 'Smart Camera 01',
    'device_type': 'smart_camera',
}
print('POST /api/devices', request('POST', '/api/devices', payload))
print('POST duplicate', request('POST', '/api/devices', payload))
print('GET /api/devices', request('GET', '/api/devices'))
print('GET /api/devices/CAM001', request('GET', '/api/devices/CAM001'))
print('GET /api/devices/UNKNOWN', request('GET', '/api/devices/UNKNOWN'))
print('DELETE /api/devices/CAM001', request('DELETE', '/api/devices/CAM001'))
print('DELETE /api/devices/CAM001 again', request('DELETE', '/api/devices/CAM001'))
