from typing_extensions import Annotated

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
)

from app.dependencies import api_key_query, get_detailed_recommender, get_plot_recommender
from app.recommender.detailed import DetailedRecommender
from app.recommender.plot import PlotRecommender

recommender_chat_router = APIRouter()


@recommender_chat_router.websocket('/plot', dependencies=[Depends(api_key_query)])
async def plot_recommendations(
    websocket: WebSocket,
    plot_recommender: Annotated[PlotRecommender, Depends(get_plot_recommender)]
):
    await websocket.accept()
    while True:
        received_data = await websocket.receive_text()
        recommendations = plot_recommender.get_recommendations(received_data)
        await websocket.send_json(recommendations.model_dump_json())


@recommender_chat_router.websocket('/detailed', dependencies=[Depends(api_key_query)])
async def detailed_recommendations(
    websocket: WebSocket,
    detailed_recommender: Annotated[DetailedRecommender, Depends(get_detailed_recommender)]
):
    await websocket.accept()
    while True:
        received_data = await websocket.receive_text()
        recommendations = detailed_recommender.get_recommendations(received_data)
        await websocket.send_json(recommendations.model_dump_json())
