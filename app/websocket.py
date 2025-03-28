from fastapi import WebSocket
from typing import Dict
from app.utils import get_timestamp


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        """Agrega un cliente a la lista de conexiones activas."""
        await websocket.accept()
        self.active_connections[websocket] = username
        await self.broadcast(f"🔵 {username} se ha conectado al chat.")
        await self.send_user_list()

    async def disconnect(self, websocket: WebSocket):
        """Elimina un cliente cuando se desconecta."""
        username = self.active_connections.pop(websocket, None)
        if username:
            await self.broadcast(f"🔴 {username} salió del chat.")
            await self.send_user_list()

    async def broadcast(self, message: str):
        """Envía un mensaje a todos los clientes conectados."""
        timestamp = get_timestamp()
        for connection in self.active_connections:
            await connection.send_text(f"{timestamp} {message}")

    async def send_private_message(self, sender: str, recipients: str, message: str):
        """Envía un mensaje privado a los destinatarios especificados."""
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
        """Envía la lista de usuarios conectados a todos los clientes."""
        user_list = ", ".join(self.active_connections.values()
                              ) or "No hay usuarios conectados."
        for connection in self.active_connections:
            await connection.send_text(f"👥 Usuarios conectados: {user_list}")


manager = ConnectionManager()
