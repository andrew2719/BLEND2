from fastapi import FastAPI, Depends
from databasing.sqlite_query import query_db
from ipfs_api import IPFS
from f_apis import router

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

# Application Routes Manager Class
class AppRoutesManager:
    def __init__(self, app: FastAPI, db_manager: DatabaseManager, ipfs_manager: IPFSManager):
        self.app = app
        self.app.include_router(router)
        self.db_manager = db_manager
        self.ipfs_manager = ipfs_manager
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/upload/{CID}")
        async def get_folder_from_ipfs(CID: str, ipfs: IPFS = Depends(self.ipfs_manager.get_ipfs), db: query_db = Depends(self.db_manager.get_db)):
            response = await ipfs.get_folder(CID)
            try:
                if response:
                    await ipfs.pin_folder(CID)
                    return await create_item(CID, db)
                else:
                    return {"error": "Folder not found"}
            except Exception as e:
                return {"error": str(e)}

        @self.app.post("/testing-upload/{CID}")
        async def testing_upload(CID: str):
            return {"CID": CID}

        async def create_item(CID: str, db: query_db):
            await db.add_entry(CID)
            return {"CID": CID}

# Main Application Class
class MyApp:
    def __init__(self):
        self.app = FastAPI()
        self.db_manager = DatabaseManager()
        self.ipfs_manager = IPFSManager()
        self.routes_manager = AppRoutesManager(self.app, self.db_manager, self.ipfs_manager)
        self.setup_event_handlers()

    def setup_event_handlers(self):
        self.app.add_event_handler("startup", self.db_manager.startup)
        self.app.add_event_handler("shutdown", self.db_manager.shutdown)
        self.app.add_event_handler("startup", self.ipfs_manager.startup)
        self.app.add_event_handler("shutdown", self.ipfs_manager.shutdown)

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    app_instance = MyApp()
    app_instance.run()
