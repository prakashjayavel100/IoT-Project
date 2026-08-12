from app.config import settings
from pymongo import MongoClient

print('raw_mongodb_uri', repr(settings.MONGODB_URI.get_secret_value()))
print('sanitized_mongodb_uri', repr(settings.mongodb_uri))
print('database_name', settings.DATABASE_NAME)
try:
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[settings.DATABASE_NAME]
    print('connected', True)
    print('collections', db.list_collection_names())
    print('devices_count', db['devices'].count_documents({}))
    print('device_analysis_count', db['device_analysis'].count_documents({}))
    print('notifications_count', db['notifications'].count_documents({}))
except Exception as exc:
    print('connected', False)
    print('error', type(exc).__name__, str(exc))
finally:
    try:
        client.close()
    except Exception:
        pass
