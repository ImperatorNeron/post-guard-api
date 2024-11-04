import pytest
from httpx import AsyncClient
from tests.api.common import (
    create_comment,
    create_post,
    register_and_login_user,
)

from app.schemas.posts import CreatePostSchema
from app.schemas.users import RegisterUserSchema


@pytest.mark.asyncio(loop_scope="session")
async def test_create_valid_comment(
    async_client: AsyncClient,
    comment_payload: CreatePostSchema,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_response = await create_post(async_client, token, post_payload)
    post_id = post_response.json()["data"]["id"]
    response = await create_comment(async_client, post_id, token, comment_payload)
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_create_invalid_comment(
    async_client: AsyncClient,
    comment_payload: CreatePostSchema,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_response = await create_post(async_client, token, post_payload)
    post_id = post_response.json()["data"]["id"]
    comment_payload.content = "You are really annoyed. F*ck off pls!!!!"
    response = await create_comment(async_client, post_id, token, comment_payload)
    assert response.status_code == 200
    assert response.json()["data"]["is_blocked"]
