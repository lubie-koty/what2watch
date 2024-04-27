from typing_extensions import Annotated

from fastapi import (
    HTTPException,
    Request,
    Security,
    WebSocketException,
    Query,
    status
)
from fastapi.security import APIKeyHeader

from app.core.config import settings
from app.recommender.detailed import DetailedRecommender
from app.recommender.plot import PlotRecommender
from app.recommender.simple import SimpleRecommender

api_key_header = APIKeyHeader(name='X-API-KEY')


async def api_key_header(api_key: str = Security(api_key_header)) -> str:
    if not api_key == settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing or invalid api key'
        )
    return api_key


async def api_key_query(key: Annotated[str | None, Query()]) -> str:
    if key is None or key != settings.API_KEY:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return key


async def get_detailed_recommender(request: Request) -> DetailedRecommender:
    return request.app.state.detailed_recommender


async def get_plot_recommender(request: Request) -> PlotRecommender:
    return request.app.state.plot_recommender


async def get_simple_recommender(request: Request) -> SimpleRecommender:
    return request.app.state.simple_recommender
