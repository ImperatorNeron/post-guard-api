from dataclasses import dataclass

from app.schemas.users import (
    ReadUserSchema,
    UpdateUserSchema,
)
from app.services.tokens import AbstractJWTTokenService
from app.services.users import AbstractUserService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class UpdateUserProfileUseCase:

    user_service: AbstractUserService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        token: str,
        uow: AbstractUnitOfWork,
        user_in: UpdateUserSchema,
    ) -> ReadUserSchema:
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:
            user = await self.user_service.update_user(
                user_id=pk,
                user_in=user_in,
                uow=uow,
            )
            return ReadUserSchema(**user.model_dump(exclude={"password"}))
