from typing_extensions import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies import api_key_header, get_detailed_recommender, get_plot_recommender
from app.recommender.detailed import DetailedRecommender
from app.recommender.plot import PlotRecommender
from app.schemas.recommendations import ChatResponse

recommender_chat_router = APIRouter()


@recommender_chat_router.get('/plot', dependencies=[Depends(api_key_header)])
async def plot_recommendations(
    movie_title: str,
    plot_recommender: Annotated[PlotRecommender, Depends(get_plot_recommender)]
) -> ChatResponse:
    return plot_recommender.get_recommendations(movie_title) 


@recommender_chat_router.get('/detailed', dependencies=[Depends(api_key_header)])
async def detailed_recommendations(
    movie_title: str,
    detailed_recommender: Annotated[DetailedRecommender, Depends(get_detailed_recommender)]
) -> ChatResponse:
    return detailed_recommender.get_recommendations(movie_title) 
