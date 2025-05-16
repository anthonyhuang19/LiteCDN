from fastapi import FastAPI
import time

server = FastAPI()

@server.get("/{path}")
async def server_content(path:str):
    delay_time = 0.5
    time.sleep(delay_time)

    return {
        "path":path,
        "server":"main",
        "processed_at":time.time(),
        "processing_time":delay_time
    }