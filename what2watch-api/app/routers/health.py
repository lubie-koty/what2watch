from fastapi import APIRouter


health_router = APIRouter()

@health_router.get('/ping')
async def ping() -> str:
    return 'OK'
