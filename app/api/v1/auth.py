from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
)
from fastapi.security import OAuth2PasswordBearer

from punq import Container

from app.core.containers import get_container
from app.schemas.api_response import ApiResponseSchema
from app.schemas.tokens import TokenInfoSchema
from app.schemas.users import (
    LoginUserSchema,
    ReadUserSchema,
    RegisterUserSchema,
)
from app.use_cases.auth.login import LoginUserUseCase
from app.use_cases.auth.registration import RegisterUserUseCase
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=ApiResponseSchema[ReadUserSchema],
)
async def register(
    user_in: RegisterUserSchema,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
):
    use_case: RegisterUserUseCase = container.resolve(RegisterUserUseCase)
    result = await use_case.execute(user_in=user_in, uow=uow)
    return ApiResponseSchema(data=result)


@router.post(
    "/login",
    response_model=TokenInfoSchema,
)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
):
    use_case: LoginUserUseCase = container.resolve(LoginUserUseCase)
    user_in = LoginUserSchema(username=username, password=password)
    return await use_case.execute(uow=uow, user_in=user_in)
