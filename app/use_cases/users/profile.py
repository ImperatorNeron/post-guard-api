from dataclasses import dataclass

from jwt import InvalidTokenError

from app.schemas.users import ReadUserSchema
from app.services.tokens import AbstractJWTTokenService
from app.services.users import AbstractUserService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class GetCurrentUserProfileUseCase:

    user_service: AbstractUserService
    token_service: AbstractJWTTokenService

    async def execute(self, token: str, uow: AbstractUnitOfWork) -> ReadUserSchema:
        try:
            payload = await self.token_service.decode_jwt(token=token)
        except InvalidTokenError as e:
            # TODO: Custom exception
            raise ValueError(f"Invalid token error: {e}")

        pk = payload.get("sub")

        async with uow:
            user = await self.user_service.get_user_by_id(
                id=pk,
                uow=uow,
            )
            return ReadUserSchema(**user.model_dump(exclude={"password"}))
