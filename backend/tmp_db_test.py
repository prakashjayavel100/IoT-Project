import sys
import asyncio
sys.path.insert(0, r'C:\IOT_Project\backend')
import app.database as database

async def main():
    try:
        await database.connect_db()
        print('connected', database.client is not None, database.db is not None)
        print('db name', database.db.name if database.db else None)
        print('ping', await database.ping_db())
    except Exception as e:
        print('ERROR', type(e).__name__, e)
    finally:
        await database.close_db()
        print('closed', database.client, database.db)

asyncio.run(main())
