from fastapi import APIRouter

from app.routers.health import health_router
from app.routers.recommender_chat import recommender_chat_router
from app.routers.recommender_ranking import recommender_ranking_router


main_router = APIRouter(prefix='/api')
main_router.include_router(recommender_chat_router, prefix='/chat')
main_router.include_router(recommender_ranking_router, prefix='/ranking')
main_router.include_router(health_router, prefix='/health')
