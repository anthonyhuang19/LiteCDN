from fastapi import FastAPI
import time

server = FastAPI()

@server.get("/{path}")
async def server_content(path:str):
    