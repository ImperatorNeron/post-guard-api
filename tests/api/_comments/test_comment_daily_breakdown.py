import pytest
from httpx import AsyncClient
from tests.api.common import (
    create_comment,
    create_post,
    register_and_login_user,
)

from app.schemas.comments import CreateCommentSchema
from app.schemas.posts import CreatePostSchema
from app.schemas.users import RegisterUserSchema


@pytest.mark.asyncio(loop_scope="session")
async def test_comment_daily_breakdown(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
    comment_payload: CreateCommentSchema,
    comments_list: list[CreateCommentSchema],
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_response = await create_post(async_client, token, post_payload)

    # wait few seconds
    post_id = post_response.json()["data"]["id"]
    for comment in comments_list:
        await create_comment(async_client, post_id, token, comment)

    comment_payload.content = "Oh, shit, this post hard to read in 4:37"

    await create_comment(async_client, post_id, token, comment_payload)

    response = await async_client.get(
        url="/api/v1/analytics/comments-daily-breakdown",
        params={
            "date_from": "2024-11-03",
            "date_to": "2025-01-01",
        },
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["created_count"] == 3
    assert response.json()["data"][0]["blocked_count"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_wrong_date_comment_daily_breakdown(
    async_client: AsyncClient,
    auth_user_payload: RegisterUserSchema,
    post_payload: CreatePostSchema,
    comments_list: list[CreateCommentSchema],
):
    token = await register_and_login_user(async_client, auth_user_payload)
    post_response = await create_post(async_client, token, post_payload)

    # wait few seconds
    post_id = post_response.json()["data"]["id"]
    for comment in comments_list:
        await create_comment(async_client, post_id, token, comment)

    response = await async_client.get(
        url="/api/v1/analytics/comments-daily-breakdown",
        params={
            "date_from": "2025-11-03",
            "date_to": "2024-01-01",
        },
    )

    assert response.status_code == 200
    assert not len(response.json()["data"])
