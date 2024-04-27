from typing_extensions import Annotated

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
)

from app.dependencies import api_key_query

chat_router = APIRouter()


@chat_router.websocket('/session', dependencies=[Depends(api_key_query)])
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)
