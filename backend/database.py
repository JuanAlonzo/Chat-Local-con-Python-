import aiosqlite

DB_NAME = "chat.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_message(username: str, content: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO messages (username, content) VALUES (?, ?)
        """, (username, content))
        await db.commit()


async def get_last_messages(limit=50):
    async with aiosqlite.connect(DB_NAME) as db:
        # Set row factory to return dict-like rows
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT username, content, timestamp FROM messages
            ORDER BY timestamp DESC LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return rows[::-1]  # Return in chronological order
