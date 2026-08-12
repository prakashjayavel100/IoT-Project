import sys
import asyncio
print('script start')
sys.path.insert(0, r'C:\IOT_Project\backend')
print('path inserted')
import app.database as database
print('imported database')
print('mongo uri:', database.settings.mongodb_uri)

async def main():
    try:
        print('connecting...')
        await database.connect_db()
        print('connected', database.client is not None, database.db is not None)
        print('db name', database.db.name if database.db else None)
        print('ping', await database.ping_db())
    except Exception as e:
        print('ERROR', type(e).__name__, e)
    finally:
        print('closing...')
        await database.close_db()
        print('closed', database.client, database.db)

asyncio.run(main())
