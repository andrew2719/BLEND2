import asyncio
import aiosqlite
import os
from typing import List, Dict, Union
from datetime import datetime

class setup_db:
    def __init__(self):
        self.db = None
    async def connect(self):
        self.db = await aiosqlite.connect(os.path.join('databasing', 'BLEND.db'))
        await self.create_tables()

    async def close(self):
        # shutdown the db
        await self.db.close()

    async def create_tables(self):

        async with self.db.execute('''
            CREATE TABLE IF NOT EXISTS ENTRY_CHECK (
                CID TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''') as cursor:
            await self.db.commit()


class query_db(setup_db):
    def __init__(self):
        super().__init__()

    @classmethod
    async def create(cls):
        instance = cls()
        await instance.connect()
        # await instance.create_tables()
        # print('DB created, tables created')
        return instance

    async def add_entry(self, cid: str):
        async with self.db.execute('''
            INSERT INTO ENTRY_CHECK (CID)
            VALUES (?)
        ''', (cid,)) as cursor:
            await self.db.commit()

    async def get_entry(self, cid: str):
        async with self.db.execute('''
            SELECT * FROM ENTRY_CHECK 
            WHERE CID = ?''', (cid,)) as cursor:
            return await cursor.fetchone()

    async def handle_old_entries(self):
#         get all the entries that are older than 1 minute
        async with self.db.execute('''
            SELECT CID FROM ENTRY_CHECK 
            WHERE timestamp < datetime('now', '-1 minute')
        ''') as cursor:
            old_entries = await cursor.fetchall()
            return old_entries

    async def remove_old_entries(self, old_entries: List[str]):
        for entry in old_entries:
            async with self.db.execute('''
                DELETE FROM ENTRY_CHECK 
                WHERE CID = ?
            ''', (entry[0],)) as cursor:
                await self.db.commit()