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
from app.use_cases.auth.registration import RegisterUserUseCase
from app.use_cases.comments.comments_by_post import GetCommentsByPostUseCase
from app.use_cases.comments.create import CreateCommentUseCase
from app.use_cases.comments.current_user_comments import GetUserCommentsUseCase
from app.use_cases.posts.create import CreatePostUseCase
from app.use_cases.posts.current_user_posts import GetUserPostsUseCase
from app.use_cases.posts.delete import DeletePostUseCase
from app.use_cases.posts.update import UpdatePostUseCase
from app.use_cases.users.personal_profile import GetCurrentUserProfileUseCase


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
    container.register(GetCurrentUserProfileUseCase)
    container.register(CreatePostUseCase)
    container.register(DeletePostUseCase)
    container.register(GetUserPostsUseCase)
    container.register(UpdatePostUseCase)
    container.register(GetCommentsByPostUseCase)
    container.register(CreateCommentUseCase)
    container.register(GetUserCommentsUseCase)

    return container
