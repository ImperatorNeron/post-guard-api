from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)
