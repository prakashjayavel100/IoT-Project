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
        try:
            return exc.code, json.loads(exc.read().decode('utf-8'))
        except Exception:
            return exc.code, exc.read().decode('utf-8')
    except Exception as exc:
        return None, {'error': str(exc)}

print('--- Device /analysis workflow ---')
reg = {'device_id':'CAM001','device_name':'Smart Camera 01','device_type':'smart_camera'}
print('register', request('POST','/api/devices',reg))
print('raw data', request('POST','/api/devices/CAM001/data',{'packet_rate':500,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('analyze', request('POST','/api/devices/CAM001/analyze',{'packet_rate':500,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('invalid negative packet', request('POST','/api/devices/CAM001/analyze',{'packet_rate':-10,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('invalid high behavior', request('POST','/api/devices/CAM001/analyze',{'packet_rate':10,'behavior_score':150,'network_score':92,'firmware_score':95}))
print('invalid string firmware', request('POST','/api/devices/CAM001/analyze',{'packet_rate':10,'behavior_score':90,'network_score':92,'firmware_score':'abc'}))
print('missing field', request('POST','/api/devices/CAM001/analyze',{'packet_rate':10,'behavior_score':90,'network_score':92}))
print('unknown device analyze', request('POST','/api/devices/UNKNOWN/analyze',{'packet_rate':10,'behavior_score':90,'network_score':92,'firmware_score':95}))
print('--- Dashboard and notification APIs ---')
print('dashboard summary', request('GET','/api/dashboard/summary'))
print('dashboard devices', request('GET','/api/dashboard/devices'))
print('device history', request('GET','/api/dashboard/devices/CAM001/history'))
print('notifications all', request('GET','/api/notifications'))
print('notifications device', request('GET','/api/notifications/CAM001'))
print('--- End ---')
