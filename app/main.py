from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.websocket import manager

# Crear una instancia de FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
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
                await manager.broadcast(f"{username}: {data}")
    except Exception as e:
        print(f"Error en Websocket: {e}")
        await manager.disconnect(websocket)


@app.get("/")
async def get():
    return RedirectResponse(url="/static/index.html")
