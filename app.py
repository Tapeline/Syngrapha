import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

from syngrapha.bootstrap.app import create_app

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

app = create_app()
