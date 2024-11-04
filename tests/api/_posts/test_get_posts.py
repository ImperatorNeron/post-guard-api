import pytest
from httpx import AsyncClient
from tests.api.common import (
    create_post,
    register_and_login_user,
)

from app.schemas.posts import CreatePostSchema
from app.schemas.users import RegisterUserSchema


@pytest.mark.asyncio(loop_scope="session")
async def test_get_empty_posts_list(
    async_client: AsyncClient,
):
    response = await async_client.get(
        url="/api/v1/posts",
    )

    assert response.status_code == 200
    assert not len(response.json()["data"])


@pytest.mark.asyncio(loop_scope="session")
async def test_get_posts_list(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
    posts_list: list[CreatePostSchema],
):
    token = await register_and_login_user(async_client, auth_user_payload)

    # wait few seconds
    for post in posts_list:
        await create_post(async_client, token, post)

    response = await async_client.get(
        url="/api/v1/posts",
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 3
