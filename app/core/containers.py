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
from app.use_cases.auth.registration import RegisterUserUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # Services
    container.register(AbstractAuthService, AuthService)
    container.register(AbstractJWTTokenService, JWTTokenService)

    # Use cases
    container.register(RegisterUserUseCase)

    return container
