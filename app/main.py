from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.api.routers import router as api_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="JunToSin API",
        docs_url="/api/docs",
        description="Starnavi test project for junior position.",
        default_response_class=ORJSONResponse,
        debug=True,
    )
    application.include_router(router=api_router)
    return application
