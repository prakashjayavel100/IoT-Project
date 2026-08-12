import urllib.request
import urllib.error
import json

BASE_URL = 'http://127.0.0.1:8001'
paths = ['/health', '/health/database']
for p in paths:
    url = BASE_URL + p
    try:
        with urllib.request.urlopen(url) as resp:
            print(p, resp.status, resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        print(p, exc.code, exc.read().decode('utf-8'))
    except Exception as exc:
        print(p, 'ERROR', exc)
