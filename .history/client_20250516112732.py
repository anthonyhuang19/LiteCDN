import pytest
from fastapi.testclient import TestClient
from app import app
from cache import CacheTable

client = TestClient(app)

def test_full_pipeline():
    print("HELLLo")
    # First request (should miss cache)
    response1 = client.get("/test")
    assert response1.status_code == 200
    assert response1.json()['metadata']['from_cache'] is False
    
    # Second request (should hit cache)
    response2 = client.get("/test")
    assert response2.status_code == 200
    assert response2.json()['metadata']['from_cache'] is True
    
    # Different path (should miss)
    response3 = client.get("/another")
    assert response3.status_code == 200
    assert response3.json()['metadata']['from_cache'] is False

def test_cache_eviction():
    cache = CacheTable(max_size=2, ttl=10)
    
    cache.set("key1", {"data": 1})
    cache.set("key2", {"data": 2})
    
    # Access key1 to make it recently used
    cache.get("key1")
    
    # Add new item (should evict key2)
    cache.set("key3", {"data": 3})
    
    assert cache.get("key1") is not None
    assert cache.get("key2") is None
    assert cache.get("key3") is not None