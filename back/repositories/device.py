import datetime

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
            return Device(id=res.id, token=res.token, notify_at=res.notify_at)
        return None

    async def add(self, d: Device) -> None:
        stmt = device.insert().values(
            id=d["id"], token=d["token"], notify_at=d["notify_at"]
        )
        await self._connection.execute(stmt)

    async def update(self, d: Device) -> None:
        stmt = (
            device.update()
            .values(token=d["token"], notify_at=d["notify_at"])
            .where(device.c.id == d["id"])
        )
        await self._connection.execute(stmt)

    async def get_devices_to_notify(self, amount: int) -> list[Device]:
        stmt = (
            device.select()
            .where(device.c.notify_at < datetime.datetime.now())
            .limit(amount)
        )
        res = await self._connection.execute(stmt)
        res = res.fetchall()
        return [Device(id=d.id, token=d.token, notify_at=d.notify_at) for d in res]
