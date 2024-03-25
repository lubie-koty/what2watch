from typing_extensions import Annotated

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketException,
    Query,
    status
)

from app.core.config import settings

chat_router = APIRouter()


async def get_api_key(
    websocket: WebSocket,
    key: Annotated[str | None, Query()],
):
    if key is None or key != settings.API_KEY:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return key


@chat_router.websocket('/session', dependencies=[Depends(get_api_key)])
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)
