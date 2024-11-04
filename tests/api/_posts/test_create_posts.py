import pytest
from httpx import AsyncClient
from tests.api.common import (
    create_post,
    register_and_login_user,
)

from app.schemas.posts import CreatePostSchema
from app.schemas.users import RegisterUserSchema


@pytest.mark.asyncio(loop_scope="session")
async def test_create_valid_post(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_response = await create_post(async_client, token, post_payload)

    assert post_response.status_code == 200
    assert not post_response.json()["data"]["is_blocked"]


@pytest.mark.asyncio(loop_scope="session")
async def test_create_invalid_post(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_payload.title = "Title about thing that I don`t f*cking care!"
    post_response = await create_post(async_client, token, post_payload)

    assert post_response.status_code == 200
    assert post_response.json()["data"]["is_blocked"]
