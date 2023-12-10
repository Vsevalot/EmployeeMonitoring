from utils import UnitOfWorkRDBS
from domain.entities import Device


class DeviceService:
    def __init__(self, uow: UnitOfWorkRDBS):
        self._uow = uow

    async def set_device_token(self, device_id: str, token: str) -> None:
        async with self._uow:
            device = await self._uow.device.get(device_id)
            if device:
                device["token"] = token
                await self._uow.device.update(device)
            else:
                device = Device(id=device_id, token=token)
                await self._uow.device.add(device)
            await self._uow.commit()
