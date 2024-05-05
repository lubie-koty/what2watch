from typing_extensions import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies import api_key_header, get_simple_recommender
from app.recommender.simple import SimpleRecommender
from app.schemas.recommendations import RecommendationList

recommender_ranking_router = APIRouter()


@recommender_ranking_router.get('/simple', dependencies=[Depends(api_key_header)])
async def simple_recommendations(
    number_of_movies: int,
    simple_recommender: Annotated[SimpleRecommender, Depends(get_simple_recommender)]
) -> RecommendationList:
    return simple_recommender.get_recommendations(number_of_movies)
