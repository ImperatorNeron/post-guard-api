from functools import lru_cache

import punq

from app.services.auth import (
    AbstractAuthService,
    AuthService,
)
from app.services.comments import (
    AbstractCommentService,
    CommentService,
)
from app.services.moderation import (
    AbstractModerationService,
    AIModerationService,
)
from app.services.posts import (
    AbstractPostService,
    PostService,
)
from app.services.tokens import (
    AbstractJWTTokenService,
    JWTTokenService,
)
from app.services.users import (
    AbstractUserService,
    UserService,
)
from app.use_cases.auth.login import LoginUserUseCase
from app.use_cases.auth.refresh import RefreshTokenUseCase
from app.use_cases.auth.registration import RegisterUserUseCase
from app.use_cases.comments.comments_by_post import GetCommentsByPostUseCase
from app.use_cases.comments.create import CreateCommentUseCase
from app.use_cases.comments.delete import DeleteCommentUseCase
from app.use_cases.comments.update import UpdateCommentUseCase
from app.use_cases.posts.create import CreatePostUseCase
from app.use_cases.posts.delete import DeletePostUseCase
from app.use_cases.posts.get_post import GetPostUseCase
from app.use_cases.posts.update import UpdatePostUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # Services
    container.register(AbstractAuthService, AuthService)
    container.register(AbstractUserService, UserService)
    container.register(AbstractPostService, PostService)
    container.register(AbstractCommentService, CommentService)
    container.register(AbstractModerationService, AIModerationService)
    container.register(AbstractJWTTokenService, JWTTokenService)

    # Use cases
    container.register(RegisterUserUseCase)
    container.register(LoginUserUseCase)
    container.register(RefreshTokenUseCase)
    container.register(CreatePostUseCase)
    container.register(DeletePostUseCase)
    container.register(UpdatePostUseCase)
    container.register(GetCommentsByPostUseCase)
    container.register(CreateCommentUseCase)
    container.register(DeleteCommentUseCase)
    container.register(GetPostUseCase)
    container.register(UpdateCommentUseCase)

    return container
