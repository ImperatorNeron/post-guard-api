from functools import lru_cache

import punq

from app.services.auth import (
    AbstractAuthService,
    AuthService,
)
from app.services.tokens import (
    AbstractJWTTokenService,
    JWTTokenService,
)
from app.services.users import AbstractUserService, UserService
from app.use_cases.auth.login import LoginUserUseCase
from app.use_cases.auth.registration import RegisterUserUseCase
from app.use_cases.users.profile import GetCurrentUserProfileUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # Services
    container.register(AbstractAuthService, AuthService)
    container.register(AbstractUserService, UserService)
    container.register(AbstractJWTTokenService, JWTTokenService)

    # Use cases
    container.register(RegisterUserUseCase)
    container.register(LoginUserUseCase)
    container.register(GetCurrentUserProfileUseCase)

    return container
