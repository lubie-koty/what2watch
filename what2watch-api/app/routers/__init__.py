from fastapi import APIRouter

from app.routers.chat import chat_router
from app.routers.health import health_router


main_router = APIRouter(prefix='/api')
main_router.include_router(chat_router, prefix='/chat')
main_router.include_router(health_router, prefix='/health')
