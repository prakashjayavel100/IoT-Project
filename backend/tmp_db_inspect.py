from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['iot_trust_db']
print('device_analysis total', db['device_analysis'].count_documents({}))
print('device_analysis valid', db['device_analysis'].count_documents({
    'anomaly_detected': {'$exists': True},
    'anomaly_score': {'$exists': True},
    'drift_detected': {'$exists': True},
    'trust_score': {'$exists': True},
    'status': {'$exists': True},
}))
print('device_analysis invalid sample')
for doc in db['device_analysis'].find({
    '$or': [
        {'anomaly_detected': {'$exists': False}},
        {'anomaly_score': {'$exists': False}},
        {'drift_detected': {'$exists': False}},
        {'trust_score': {'$exists': False}},
        {'status': {'$exists': False}},
    ]
}).limit(5):
    print(doc)
