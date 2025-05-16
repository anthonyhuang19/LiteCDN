'''
This application using for handling cache, client request -> cache handle  : 1. will ask cache " is there any 
'''
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from cache import CacheTable
import httpx
import time

app = FastAPI()
cache = CacheTable(max_size=5, ttl=10)  # Small values for demo

@app.get("/{path:path}")
async def handle_request(request: Request, path: str):
    # Create unique cache key
    cache_key = f"{request.method}:{path}"
    
    # Check cache
    if cached_data := cache.get(cache_key):
        print(f"Cache HIT for {path}")
        return JSONResponse({
            "data": cached_data,
            "metadata": {
                "from_cache": True,
                "cache_key": cache_key,
                "timestamp": time.time()
            }
        })
    
    print(f"Cache MISS for {path}")
    
    # Forward to main server
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:8000/{path}",
                timeout=2.0
            )
            
            if response.status_code == 200:
                # Cache successful responses
                cache.set(cache_key, response.json())
                cache.print_cache()  # For learning
                
                return JSONResponse({
                    "data": response.json(),
                    "metadata": {
                        "from_cache": False,
                        "cache_key": cache_key,
                        "timestamp": time.time()
                    }
                })
            else:
                raise HTTPException(response.status_code)
                
    except httpx.RequestError as e:
        raise HTTPException(502, detail=f"Backend error: {str(e)}")