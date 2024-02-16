import aioipfs
import asyncio
import aiofiles


class IPFS:
    def __init__(self):
        self.client = aioipfs.AsyncIPFS(maddr='/ip4/127.0.0.1/tcp/5001')

    async def add_folder(self, folder):
        async for added in self.client.core.add(folder, recursive=True, wrap_with_directory=True):
            print(added)

    async def get_folder(self, folder_hash):
        try:
            await self.client.get(folder_hash, dstdir='downloads')
            return True
        except Exception as e:
            # print(e)
            return False


    async def pin_folder(self, folder_hash):
        async for pinned in self.client.pin.add(folder_hash,recursive=True):
            print(pinned)

    async def unpin_folder(self, folder_hash):
        await self.client.pin.rm(folder_hash)
        print('Pin removed')

    async def close(self):
        await self.client.close()

