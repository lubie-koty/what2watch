from typing_extensions import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import Settings

api_key_header = APIKeyHeader(name='X-API-KEY')


def api_key_check(api_key: Annotated[str, Security(api_key_header)]) -> str:
    if not api_key == Settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing or invalid api key'
        )
    return api_key
