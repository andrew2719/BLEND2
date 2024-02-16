
from fastapi import APIRouter,Depends
from ipfs_api import IPFS as ipfs



class APIS:
    def __init__(self,db,ipfs):
        self.router = APIRouter()
        self.db_manager = db
        self.ipfs_manager = ipfs
        self.setup_routes()
    def return_router(self):
        return self.router
    def setup_routes(self):
        @self.router.get("/")
        async def root():
            return {"message": "Hello World"}
        @self.router.post("/test/{cid}")
        async def hello(cid,db = Depends(self.db_manager.get_db)):
            await db.add_entry(cid)
            return {"CID": cid}

        @self.router.post("/upload/{CID}")
        async def get_method_ipfs(CID:str, ipfs=Depends(self.ipfs_manager.get_ipfs), db=Depends(self.db_manager.get_db)):
            response = await ipfs.get_folder(CID)
            try:
                if response:
                    await ipfs.pin_folder(CID)
                    return await create_item(CID, db)
                else:
                    return {"error": "Folder not found"}
            except Exception as e:
                return {"error": str(e)}

        async def create_item(CID, db):
            await db.add_entry(CID)
            return {"CID": CID}