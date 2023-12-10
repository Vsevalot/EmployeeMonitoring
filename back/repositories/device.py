from sqlalchemy.ext.asyncio import AsyncConnection
from domain.entities import Device
from ports.rdbs.generic import device


class DeviceRepositoryRDBS:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def get(self, id: str) -> Device | None:
        stmt = device.select().where(device.c.id == id)
        res = await self._connection.execute(stmt)
        res = res.fetchone()
        if res:
            return Device(id=res.id, token=res.token)
        return None

    async def add(self, d: Device) -> None:
        stmt = device.insert().values(id=d["id"], token=d["token"])
        await self._connection.execute(stmt)

    async def update(self, d: Device) -> None:
        stmt = device.update().values(token=d["token"]).where(device.c.id == d["id"])
        await self._connection.execute(stmt)
