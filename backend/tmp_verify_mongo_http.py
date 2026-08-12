import json
from pymongo import MongoClient
import urllib.request
import urllib.error

print('http_health:')
try:
    with urllib.request.urlopen('http://127.0.0.1:8003/health', timeout=10) as resp:
        print(resp.status)
        print(resp.read().decode('utf-8'))
except Exception as exc:
    print(type(exc).__name__, exc)

print('http_docs:')
try:
    with urllib.request.urlopen('http://127.0.0.1:8003/docs', timeout=10) as resp:
        print(resp.status)
        body = resp.read().decode('utf-8')
        print(body[:200].replace('\n',' '))
except Exception as exc:
    print(type(exc).__name__, exc)

print('mongo:')
try:
    client = MongoClient('mongodb://127.0.0.1:27017', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client['iot_trust_db']
    print(json.dumps({
        'collections': db.list_collection_names(),
        'devices': db['devices'].count_documents({}),
        'analysis': db['device_analysis'].count_documents({}),
    }))
except Exception as exc:
    print(type(exc).__name__, exc)
finally:
    try:
        client.close()
    except Exception:
        pass
