''''
So this is the main server, so for example, you are using google or baidu.com , you will send https server req to main server, after that 
the main server reply like return the package to 
'''
from fastapi import FastAPI
import time

server = FastAPI()

@server.get("/{path}")
async def server_content(path:str):
    print(path)
    delay_time = 0.5
    time.sleep(delay_time)

    return {
        "path":path,
        "server":"main",
        "processed_at":time.time(),
        "processing_time":delay_time
    }

@server.get("/")
async def root():
    return {"message": "main server is running"}