import urllib.request
import urllib.error
import json

def request(path, method='GET', data=None):
    url = 'http://127.0.0.1:8000' + path
    body = None
    headers = {}
    if data is not None:
        body = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode('utf-8')
    except urllib.error.HTTPError as ex:
        return ex.code, ex.read().decode('utf-8')
    except Exception as ex:
        return None, str(ex)

paths = ['/health', '/health/database']
for p in paths:
    status, body = request(p)
    print('PATH', p)
    print('STATUS', status)
    print('BODY', body)
    print('---')
