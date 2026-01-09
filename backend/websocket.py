from fastapi import WebSocket
from typing import Dict
from backend.database import save_message, get_last_messages
from backend.utils import get_timestamp


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        if username in self.active_connections.values():
            await websocket.close(code=4000, reason="Nombre de usuario ya en uso.")
            return False

        await websocket.accept()
        self.active_connections[websocket] = username

        history = await get_last_messages()
        for msg in history:
            time_str = msg['timestamp'][11:16]
            await websocket.send_text(
                f"[{time_str}] {msg['username']}: {msg['content']}"
            )

        await self.broadcast(f"🔵 {username} se ha conectado al chat.")
        await self.send_user_list()
        return True

    async def disconnect(self, websocket: WebSocket):
        """Elimina un cliente cuando se desconecta."""
        username = self.active_connections.pop(websocket, None)
        if username:
            await self.broadcast(f"🔴 {username} salió del chat.")
            await self.send_user_list()

    async def broadcast(self, message: str, sender: str = None):
        if sender:
            await save_message(sender, message)
            display_text = f"{sender}: {message}"
        else:
            display_text = message

        timestamp = get_timestamp()
        final_message = f"{timestamp} {display_text}"

        for connection in self.active_connections:
            await connection.send_text(final_message)

    async def send_private_message(self, sender: str, recipients: str, message: str):
        recipients = [r.strip() for r in recipients.split(",")
                      ]  # Separar múltiples destinatarios
        for recipient in recipients:
            for ws, user in self.active_connections.items():
                if user == recipient:
                    await ws.send_text(f"🔒 {sender} (privado): {message}")
                    break
            else:
                for ws, user in self.active_connections.items():
                    if user == sender:
                        await ws.send_text(f"⚠️ Usuario '{recipient}' no encontrado.")

    async def send_user_list(self):
        user_list = ", ".join(self.active_connections.values()
                              ) or "No hay usuarios conectados."
        for connection in self.active_connections:
            await connection.send_text(f"👥 Usuarios conectados: {user_list}")


manager = ConnectionManager()
