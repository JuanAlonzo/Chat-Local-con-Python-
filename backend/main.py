from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from contextlib import asynccontextmanager
from backend.database import init_db
from backend.websocket import manager
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    is_connected = await manager.connect(websocket, username)
    if not is_connected:
        return
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("@"):
                parts = data.split(" ", 1)
                if len(parts) > 1:
                    recipient, message = parts
                    await manager.send_private_message(username, recipient[1:], message)
                else:
                    await websocket.send_text("⚠️ Formato incorrecto. Usa '@usuario' mensaje.")
            else:
                await manager.broadcast(message=data, sender=username)
    except Exception as e:
        print(f"Error o desconexión: {e}")
        await manager.disconnect(websocket)

# En desarrollo

frontend_dist = os.path.join(os.path.dirname(__file__), "../frontend/dist")

if os.path.exists(frontend_dist):
    app.mount(
        "/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        else:
            return FileResponse(os.path.join(frontend_dist, "index.html"))

else:
    @app.get("/")
    async def msg():
        return {"message": "Frontend no encontrado. Por favor, construye el frontend y colócalo en la carpeta 'frontend/dist'."}
