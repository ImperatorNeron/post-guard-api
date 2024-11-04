import pytest
from tests.factories.comments import CommentFactory
from tests.factories.posts import PostFactory
from tests.factories.users import AuthUserPayloadFactory


@pytest.fixture
async def auth_user_payload():
    return AuthUserPayloadFactory()


@pytest.fixture
async def post_payload():
    return PostFactory()


@pytest.fixture
async def comment_payload():
    return CommentFactory()


@pytest.fixture
async def posts_list():
    return PostFactory.create_batch(3)


@pytest.fixture
async def comments_list():
    return CommentFactory.create_batch(3)
