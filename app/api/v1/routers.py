from fastapi import APIRouter

from app.api.v1.analytics import router as analytics
from app.api.v1.auth import router as auth
from app.api.v1.comments import router as comments
from app.api.v1.posts import router as posts
from app.api.v1.users import router as users


router = APIRouter(prefix="/v1")
router.include_router(router=auth)
router.include_router(router=users)
router.include_router(router=posts)
router.include_router(router=comments)
router.include_router(router=analytics)
