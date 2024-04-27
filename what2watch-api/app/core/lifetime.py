from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.recommender.detailed import DetailedRecommender
from app.recommender.plot import PlotRecommender
from app.recommender.simple import SimpleRecommender


def load_recommenders(app: FastAPI) -> None:
    # detailed_recommender = DetailedRecommender()
    # app.state.detailed_recommender = detailed_recommender
    plot_recommender = PlotRecommender()
    app.state.plot_recommender = plot_recommender
    simple_recommender = SimpleRecommender()
    app.state.simple_recommender = simple_recommender


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_recommenders(app)
    yield
    # clear ML models
