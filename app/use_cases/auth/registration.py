from dataclasses import dataclass

from app.schemas.users import (
    CreateUserSchema,
    ReadUserSchema,
    RegisterUserSchema,
)
from app.services.auth import AbstractAuthService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class RegisterUserUseCase:
    auth_service: AbstractAuthService
    token_service: AbstractJWTTokenService

    async def __register_user(
        self,
        user_in: RegisterUserSchema,
        uow: AbstractUnitOfWork,
    ) -> ReadUserSchema:
        user_auth_in = CreateUserSchema(
            **user_in.model_dump(exclude={"password"}),
            hashed_password=await self.token_service.hash_password(user_in.password),
        )
        return await self.auth_service.register(
            uow,
            user_auth_in,
        )

    async def execute(
        self,
        user_in: RegisterUserSchema,
        uow: AbstractUnitOfWork,
    ) -> ReadUserSchema:
        async with uow:
            return await self.__register_user(user_in=user_in, uow=uow)
