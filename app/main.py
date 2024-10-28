from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


def create_app() -> FastAPI:
    application = FastAPI(
        title="JunToSin API",
        docs_url="/api/docs",
        description="Starnavi test project for junior position.",
        default_response_class=ORJSONResponse,
        debug=True,
    )
    return application
