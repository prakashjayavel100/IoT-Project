from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['iot_trust_db']
filter = {
    'device_id': 'CAM001',
    'anomaly_detected': {'$exists': True},
    'anomaly_score': {'$exists': True},
    'drift_detected': {'$exists': True},
    'trust_score': {'$exists': True},
    'status': {'$exists': True},
}
print('query', filter)
for doc in db['device_analysis'].find(filter).sort('timestamp', -1).limit(10):
    print(doc)
print('count', db['device_analysis'].count_documents(filter))
