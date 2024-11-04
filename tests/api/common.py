import pytest
from httpx import AsyncClient

from app.schemas.posts import CreatePostSchema
from app.schemas.users import (
    LoginUserSchema,
    RegisterUserSchema,
)


@pytest.mark.asyncio(loop_scope="session")
async def register_and_login_user(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
) -> str:
    user_response = await async_client.post(
        url="/api/v1/auth/register",
        json=auth_user_payload.model_dump(mode="json"),
    )
    assert user_response.status_code == 200

    login_credentials = LoginUserSchema(
        username=auth_user_payload.username,
        password=auth_user_payload.password,
    )
    login_response = await async_client.post(
        url="/api/v1/auth/login",
        data=login_credentials.model_dump(mode="json"),
    )
    assert login_response.status_code == 200

    return login_response.json()["access_token"]


@pytest.mark.asyncio(loop_scope="session")
async def create_post(
    async_client: AsyncClient,
    token: str,
    post_payload: CreatePostSchema,
):
    post_response = await async_client.post(
        url="/api/v1/posts",
        json=post_payload.model_dump(mode="json"),
        headers={"Authorization": f"Bearer {token}"},
    )
    return post_response


@pytest.mark.asyncio(loop_scope="session")
async def create_comment(
    async_client: AsyncClient,
    post_id: int,
    token: str,
    comment_payload: CreatePostSchema,
):
    comment_response = await async_client.post(
        url=f"/api/v1/comments/posts/{post_id}",
        json=comment_payload.model_dump(mode="json"),
        headers={"Authorization": f"Bearer {token}"},
    )
    return comment_response
