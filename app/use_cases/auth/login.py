from dataclasses import dataclass

from app.exceptions.auth import InvalidCredentialsError
from app.exceptions.users import UserWasNotFoundError
from app.schemas.tokens import TokenInfoSchema
from app.schemas.users import (
    LoginUserSchema,
    ReadUserWithPasswordSchema,
)
from app.services.tokens import AbstractJWTTokenService
from app.services.users import AbstractUserService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class LoginUserUseCase:

    user_service: AbstractUserService
    token_service: AbstractJWTTokenService

    async def __fetch_user_by_username(
        self,
        uow: AbstractUnitOfWork,
        username: str,
    ) -> ReadUserWithPasswordSchema:
        user: ReadUserWithPasswordSchema = await self.user_service.get_user_by_username(
            uow=uow,
            username=username,
        )

        if not user:
            raise UserWasNotFoundError()

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

    async def __generate_token(
        self,
        pk: int,
        username: str,
    ) -> TokenInfoSchema:
        payload = {"sub": pk, "username": username}
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
                raise InvalidCredentialsError()

            return await self.__generate_token(
                pk=user.id,
                username=user.username,
            )
