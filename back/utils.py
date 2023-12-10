from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncEngine

from repositories.device import DeviceRepositoryRDBS
from repositories.user import UserRepositoryRDBS
from repositories.company import CompanyRepositoryRDBS
from repositories.business_unit import BusinessUnitRepositoryRDBS
from repositories.session import SessionRepositoryRDBS
from repositories.category import CategoryRepositoryRDBS
from repositories.state import StateRepositoryRDBS
from repositories.feedback import FeedbackRepositoryRDBS


class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class UnitOfWorkRDBS(UnitOfWork):
    user: UserRepositoryRDBS
    company: CompanyRepositoryRDBS
    business_unit: BusinessUnitRepositoryRDBS
    session: SessionRepositoryRDBS
    category: CategoryRepositoryRDBS
    state: StateRepositoryRDBS
    feedback: FeedbackRepositoryRDBS
    device: DeviceRepositoryRDBS

    def __init__(self, connection_fabric: AsyncEngine):
        self._connection_fabric = connection_fabric

    async def __aenter__(self):
        self._conn = await self._connection_fabric.connect()
        self.user = UserRepositoryRDBS(self._conn)
        self.company = CompanyRepositoryRDBS(self._conn)
        self.business_unit = BusinessUnitRepositoryRDBS(self._conn)
        self.session = SessionRepositoryRDBS(self._conn)
        self.category = CategoryRepositoryRDBS(self._conn)
        self.state = StateRepositoryRDBS(self._conn)
        self.device = DeviceRepositoryRDBS(self._conn)
        self.feedback = FeedbackRepositoryRDBS(self._conn)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._conn.rollback()
        await self._conn.close()

    async def commit(self) -> None:
        await self._conn.commit()

    async def rollback(self) -> None:
        await self._conn.rollback()
