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
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode('utf-8')
    except urllib.error.HTTPError as ex:
        return ex.code, ex.read().decode('utf-8')
    except Exception as ex:
        return None, str(ex)


def print_result(label, status, body):
    print('---', label, '---')
    print('status=', status)
    print(body)


print_result('health', *request('GET', '/health'))
print_result('docs', *request('GET', '/docs'))
print_result('device register', *request('POST', '/api/devices', {'device_id': 'DEMO001', 'device_name': 'Smart Camera Demo', 'device_type': 'smart_camera'}))
print_result('device list', *request('GET', '/api/devices'))
print_result('device get', *request('GET', '/api/devices/DEMO001'))
print_result('device duplicate', *request('POST', '/api/devices', {'device_id': 'DEMO001', 'device_name': 'Smart Camera Demo', 'device_type': 'smart_camera'}))
print_result('device data', *request('POST', '/api/devices/DEMO001/data', {'packet_rate': 500, 'behavior_score': 90, 'network_score': 92, 'firmware_score': 95}))
print_result('analysis normal', *request('POST', '/api/devices/DEMO001/analyze', {'packet_rate': 500, 'behavior_score': 90, 'network_score': 92, 'firmware_score': 95}))
print_result('dashboard summary', *request('GET', '/api/dashboard/summary'))
print_result('dashboard devices', *request('GET', '/api/dashboard/devices'))
print_result('dashboard history', *request('GET', '/api/dashboard/devices/DEMO001/history'))
print_result('notifications', *request('GET', '/api/notifications'))
print_result('notifications device', *request('GET', '/api/notifications/DEMO001'))
