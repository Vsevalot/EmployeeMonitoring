from domain.contracts import IdentifierType


class TokenService:
    async def get_token_for_user(self, user_id: IdentifierType) -> str:
        return "test_token"
