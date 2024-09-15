import aiomysql
import contextlib


@contextlib.asynccontextmanager
async def connect():
    conn = await aiomysql.connect(
        host="37.114.46.3",
        user="botaccount",
        password="widder25.03",
        db="planetbot",
        autocommit=True
    )
    async with conn.cursor() as cur:
        yield conn, cur
    conn.close()
