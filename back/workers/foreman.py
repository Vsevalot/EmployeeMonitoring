import asyncio
from typing import NoReturn
import time

from sqlalchemy.ext.asyncio import create_async_engine
import schedule

from services import DeviceService
from config import DBConfig
from services.notification import NotificationService
from utils import UnitOfWorkRDBS
from lggr import logger


class Foreman:
    def __init__(
        self,
        device_service: DeviceService,
        notification_service: NotificationService,
    ):
        self._device_service = device_service
        self._notification_service = notification_service

    def run(self) -> NoReturn:
        schedule.every(5).seconds.do(self._run)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def _run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self._device_service.notify_devices(
                notification_service=self._notification_service
            )
        )


def bootstrap_worker(db_config: DBConfig, path_to_cert: str) -> Foreman:
    engine = create_async_engine(db_config.dsn)
    uow = UnitOfWorkRDBS(connection_fabric=engine)
    device_service = DeviceService(uow)

    notification_service = NotificationService(path_to_cert=path_to_cert, logger=logger)
    return Foreman(
        device_service=device_service,
        notification_service=notification_service,
    )
