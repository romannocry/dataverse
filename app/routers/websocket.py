from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets import manager

ws_router = APIRouter()

@ws_router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        print("Client disconnected")
        manager.disconnect(websocket)