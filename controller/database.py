import asyncio
import copy
from contextlib import asynccontextmanager

lock = asyncio.Lock()

class Session():
    def __init__(self, db):
        self.db = db

    def get_all_positions(self):
        return copy.deepcopy(
            self.db['positions']
        )

    def get_positions(self, stock):
        return copy.deepcopy(
            self.db['positions'].get(stock, {})
        )

    def update_positions(self, stock, positions):
        self.db['positions'][stock] = positions

    def get_splits(self):
        return copy.deepcopy(
            self.db['splits']
        )

    def update_splits(self, splits):
        self.db['splits'] = splits


class Database():
    def __init__(self):
        self.db = {
            'positions': {},
            'splits': {}
        }

    @asynccontextmanager
    async def lock(self):
        await lock.acquire()
        try:
            yield Session(self.db)
        finally:
            lock.release()

