import datetime

from services.notification import NotificationService
from utils import UnitOfWorkRDBS
from domain.entities import Device
from config import MORNING_NOTIFY_TIME, EVENING_NOTIFY_TIME, NOTIFICATION_BODY, NOTIFICATION_TITLE


def get_next_notification_time() -> datetime.datetime:
    now = datetime.datetime.now()
    if MORNING_NOTIFY_TIME.hour < now.hour < EVENING_NOTIFY_TIME.hour:
        return now.replace(hour=EVENING_NOTIFY_TIME.hour)
    tomorrow = now + datetime.timedelta(days=1)
    return tomorrow.replace(hour=MORNING_NOTIFY_TIME.hour)


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
                device = Device(
                    id=device_id, token=token, notify_at=get_next_notification_time()
                )
                await self._uow.device.add(device)
            await self._uow.commit()

    async def notify_devices(
        self,
        notification_service: NotificationService,
        amount: int = 100,
    ) -> None:
        async with self._uow:
            devices = await self._uow.device.get_devices_to_notify(amount)
            for d in devices:
                try:
                    notification_service.notify(
                        title=NOTIFICATION_TITLE,
                        body=NOTIFICATION_BODY,
                        device_token=d["token"],
                    )
                    print(f"Notified device {d['id']}")
                except Exception as e:
                    print(f"Can't notify {d['id']} reason: {e}")
                finally:
                    d["notify_at"] = get_next_notification_time()
                    await self._uow.device.update(d)
            await self._uow.commit()
            if devices:
                print("All devices notified")
