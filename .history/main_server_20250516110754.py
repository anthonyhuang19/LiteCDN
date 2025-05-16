from fastapi import FastAPI
import time

server = FastAPI()

@server.get()