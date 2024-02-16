from fastapi import FastAPI, Depends
from databasing.sqlite_query import query_db
from ipfs_api import IPFS
from f_apis import APIS
from logger import fast_api_logger as flog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests

# Database Manager Class
class DatabaseManager:
    def __init__(self):
        self.db_instance = None

    async def startup(self):
        self.db_instance = await query_db.create()

    async def shutdown(self):
        await self.db_instance.close()
        self.db_instance = None

    async def get_db(self):
        return self.db_instance

# IPFS Manager Class
class IPFSManager:
    def __init__(self):
        self.ipfs = None

    async def startup(self):
        self.ipfs = IPFS()

    async def shutdown(self):
        await self.ipfs.close()
        self.ipfs = None

    async def get_ipfs(self):
        return self.ipfs


class PeerManager:
    def __init__(self, db_manager: DatabaseManager):
        self.peers = [
            "10.10.11.126",
            "10.10.11.125"
        ]
        self.scheduler = AsyncIOScheduler()
        self.db = db_manager

    async def startup(self):
        self.scheduler.add_job(self.check_db, "interval", minutes = 2)
        self.scheduler.start()

    async def shutdown(self):
        self.scheduler.shutdown()

    async def check_db(self):
        flog.info("checking db")
    #     db = await self.db.get_db()
    #     old_entries = await db.handle_old_entries()
    #     cids = []
    #     for i in old_entries:
    #         for entry in i:
    #             cids.append(entry)
    #
    #     try:
    # #         url : http://<ip>:8000/{cid}
    #         for peer in self.peers:
    #             for cid in cids:
    #                 await self.inform(peer, cid)
    #     except Exception as e:
    #         flog.error(e)
    #
    #     finally:
    #         cids = []


    async def inform(self, peer, cid):
        url = f"http://{peer}:8000/{cid}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                flog.info(f"Peer {peer} has been informed about CID: {cid}")
        except Exception as e:
            flog.error(e)



# Application Routes Manager Class
class AppRoutesManager:
    def __init__(self, app: FastAPI, db_manager: DatabaseManager, ipfs_manager: IPFSManager):
        self.app = app
        self.app.include_router(APIS(db_manager,ipfs_manager).return_router())
        self.db_manager = db_manager
        self.ipfs_manager = ipfs_manager
        self.setup_routes()

    def setup_routes(self):
        pass


# Main Application Class
class MyApp:
    def __init__(self):
        self.app = FastAPI()
        self.db_manager = DatabaseManager()
        self.ipfs_manager = IPFSManager()
        self.scheduler = AsyncIOScheduler()
        self.peer_manager = PeerManager(self.db_manager)
        self.routes_manager = AppRoutesManager(self.app, self.db_manager, self.ipfs_manager)

        self.setup_all_event_handlers()

    def setup_all_event_handlers(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, 'startup') and callable(getattr(attr, 'startup')):
                self.app.add_event_handler("startup", getattr(attr, 'startup'))
            if hasattr(attr, 'shutdown') and callable(getattr(attr, 'shutdown')):
                self.app.add_event_handler("shutdown", getattr(attr, 'shutdown'))

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    app_instance = MyApp()
    app_instance.run()
