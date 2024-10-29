from dataclasses import dataclass

from app.schemas.tokens import TokenInfoSchema
from app.schemas.users import (
    LoginUserSchema,
    ReadUserWithPasswordSchema,
)
from app.services.auth import AbstractAuthService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class LoginUserUseCase:

    auth_service: AbstractAuthService
    token_service: AbstractJWTTokenService

    async def __fetch_user_by_username(
        self,
        uow: AbstractUnitOfWork,
        username: str,
    ) -> ReadUserWithPasswordSchema:
        user: ReadUserWithPasswordSchema = await self.auth_service.get_user_by_username(
            uow=uow,
            username=username,
        )

        # TODO: custom error
        if not user:
            raise ValueError("User wasn`t found")

        return user

    def __is_valid_password(
        self,
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return self.token_service.validate_password(
            password=password,
            hashed_password=hashed_password,
        )

    async def __generate_token(self, username: str) -> TokenInfoSchema:
        payload = {"sub": username}
        token = await self.token_service.encode_jwt(payload=payload)

        return TokenInfoSchema(
            access_token=token,
            token_type="Bearer",
        )

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        user_in: LoginUserSchema,
    ):
        async with uow:
            user = await self.__fetch_user_by_username(
                uow=uow,
                username=user_in.username,
            )

            if not self.__is_valid_password(
                user_in.password,
                user.hashed_password,
            ):
                raise ValueError("Invalid credentials")

            return await self.__generate_token(user_in.username)
