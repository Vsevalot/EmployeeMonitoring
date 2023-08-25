from domain.contracts import IdentifierType, Token
from utils import UnitOfWorkRDBS


class TokenService:
    def __init__(self, uow: UnitOfWorkRDBS):
        self._uow = uow

    async def get_new_token(self, user_id: IdentifierType) -> Token:
        async with self._uow:
            await self._uow.session.delete_sessions(user_id)
            token = await self._uow.session.add_session(user_id)
            await self._uow.commit()
        return token

    async def get_user_id(self, token: Token) -> IdentifierType:
        async with self._uow:
            return await self._uow.session.get_user_id(token)
