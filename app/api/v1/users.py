from typing import Annotated
from fastapi import APIRouter, Depends
from punq import Container

from app.core.containers import get_container
from app.schemas.users import ReadUserSchema
from app.use_cases.users.profile import GetCurrentUserProfileUseCase
from app.utils.unit_of_work import AbstractUnitOfWork, UnitOfWork
from app.api.v1.dependencies import oauth2_scheme


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=ReadUserSchema,
)
async def get_authenticated_user_profile(
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    use_case: GetCurrentUserProfileUseCase = container.resolve(
        GetCurrentUserProfileUseCase,
    )
    return await use_case.execute(token=token, uow=uow)
