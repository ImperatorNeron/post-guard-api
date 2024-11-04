import pytest
from httpx import AsyncClient
from tests.api.common import (
    create_post,
    register_and_login_user,
)

from app.schemas.posts import (
    CreatePostSchema,
    UpdatePostSchema,
)
from app.schemas.users import RegisterUserSchema


@pytest.mark.asyncio(loop_scope="session")
async def test_valid_update_post(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_response = await create_post(async_client, token, post_payload)
    post_id = post_response.json()["data"]["id"]

    update_payload = UpdatePostSchema(
        title="New great title",
        content="Greate content",
    )

    update_response = await async_client.patch(
        url=f"/api/v1/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_payload.model_dump(mode="json"),
    )

    assert update_response.status_code == 200

    updated_data = update_response.json()["data"]
    assert updated_data["title"] == update_payload.title
    assert not updated_data["is_blocked"]


@pytest.mark.asyncio(loop_scope="session")
async def test_invalid_update_post(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_response = await create_post(async_client, token, post_payload)
    post_id = post_response.json()["data"]["id"]

    update_payload = UpdatePostSchema(
        title="New f*cking title",
        content="Not greate content",
    )

    update_response = await async_client.patch(
        url=f"/api/v1/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_payload.model_dump(mode="json"),
    )

    assert update_response.status_code == 200

    updated_data = update_response.json()["data"]
    assert updated_data["title"] == update_payload.title
    assert updated_data["is_blocked"]
