import pytest
from fastapi.testclient import TestClient
from app import app
from cache import CacheTable
import time

client = TestClient(app)

def test_full_pipeline():
    response1 = client.get("/test")
    assert response1.status_code == 200
    assert response1.json()['metadata']['from_cache'] is False

    response2 = client.get("/test")
    assert response2.status_code == 200
    assert response2.json()['metadata']['from_cache'] is True

    response3 = client.get("/another")
    assert response3.status_code == 200
    assert response3.json()['metadata']['from_cache'] is False

    response4 = client.get("/another")
    assert response4.status_code == 200
    assert response4.json()['metadata']['from_cache'] is True

def test_cache_eviction():
    cache = CacheTable(max_size=2, ttl=100)
    cache.set("key1", {"data": 1})
    cache.set("key2", {"data": 2})
    cache.get("key1")
    cache.set("key3", {"data": 3})
    assert cache.get("key1") is not None
    assert cache.get("key2") is None
    assert cache.get("key3") is not None

def test_cache_ttl_expiration():
    cache = CacheTable(max_size=2, ttl=1)
    cache.set("key1", {"data": 1})
    time.sleep(1.5)
    assert cache.get("key1") is None

def test_cache_overwrite_same_key():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("key1", {"data": 1})
    cache.set("key1", {"data": 2})
    value = cache.get("key1")
    assert value is not None
    assert value['data'] == 2

def test_cache_lru_order():
    cache = CacheTable(max_size=3, ttl=100)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    cache.get("a")
    cache.set("d", 4)
    assert cache.get("a") == 1
    assert cache.get("b") is None
    assert cache.get("c") == 3
    assert cache.get("d") == 4
