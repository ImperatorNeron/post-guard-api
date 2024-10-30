from fastapi import APIRouter

from app.api.v1.auth import router as auth
from app.api.v1.users import router as users


router = APIRouter(prefix="/v1")
router.include_router(router=auth)
router.include_router(router=users)
