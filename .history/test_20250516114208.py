import time
import pytest
from fastapi.testclient import TestClient
from app import app
from cache import CacheTable

client = TestClient(app)


# 1-5: Basic cache hit/miss tests
def test_01_cache_miss_then_hit():
    r1 = client.get("/test1")
    assert r1.status_code == 200
    assert r1.json()['metadata']['from_cache'] is False
    r2 = client.get("/test1")
    assert r2.status_code == 200
    assert r2.json()['metadata']['from_cache'] is True

def test_02_different_paths_cache():
    r1 = client.get("/a")
    r2 = client.get("/b")
    r3 = client.get("/a")
    assert r1.json()['metadata']['from_cache'] is False
    assert r2.json()['metadata']['from_cache'] is False
    assert r3.json()['metadata']['from_cache'] is True

def test_03_cache_eviction_order():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"val": 1})
    cache.set("k2", {"val": 2})
    cache.get("k1")
    cache.set("k3", {"val": 3})  # should evict k2
    assert cache.get("k1") is not None
    assert cache.get("k2") is None
    assert cache.get("k3") is not None

def test_04_cache_ttl_expiry():
    cache = CacheTable(max_size=2, ttl=1)
    cache.set("key", {"val": 1})
    assert cache.get("key") is not None
    time.sleep(1.1)
    assert cache.get("key") is None

def test_05_cache_touch_updates_access():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"val": 1})
    old_access = cache.cache["k1"]['last_accessed']
    time.sleep(0.1)
    cache.touch("k1")
    assert cache.cache["k1"]['last_accessed'] > old_access


# 6-15: More cache edge cases and API behavior
def test_06_empty_key_handling():
    cache = CacheTable(max_size=2, ttl=10)
    assert cache.get("") is None
    cache.set("", {"val": 0})
    assert cache.get("") is not None

def test_07_large_value_storage():
    large_val = {"data": "x" * 10_000}
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("large", large_val)
    assert cache.get("large") == large_val

def test_08_eviction_multiple_times():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"v": 1})
    cache.set("k2", {"v": 2})
    cache.get("k1")
    cache.set("k3", {"v": 3})  # evict k2
    cache.set("k4", {"v": 4})  # evict k1
    assert cache.get("k2") is None
    assert cache.get("k1") is None
    assert cache.get("k3") is not None
    assert cache.get("k4") is not None

def test_09_api_root_endpoint():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

def test_10_api_cache_independent_paths():
    r1 = client.get("/path1")
    r2 = client.get("/path2")
    assert not r1.json()['metadata']['from_cache']
    assert not r2.json()['metadata']['from_cache']


# 16-25: More API cache tests, including timing and error handling
def test_11_api_cache_hit_and_miss():
    r1 = client.get("/cache_test")
    r2 = client.get("/cache_test")
    assert not r1.json()['metadata']['from_cache']
    assert r2.json()['metadata']['from_cache']

def test_12_cache_eviction_respects_ttl():
    cache = CacheTable(max_size=2, ttl=1)
    cache.set("k1", {"v": 1})
    cache.set("k2", {"v": 2})
    time.sleep(1.1)
    cache.set("k3", {"v": 3})
    # All expired so none evicted but oldest removed
    assert cache.get("k1") is None
    assert cache.get("k2") is None
    assert cache.get("k3") is not None

def test_13_cache_set_overwrites():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"v": 1})
    cache.set("k1", {"v": 2})
    assert cache.get("k1") == {"v": 2}

def test_14_cache_print_cache_runs_without_error():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"v": 1})
    cache.print_cache()  # Just test no crash

def test_15_cache_delete_after_expiry():
    cache = CacheTable(max_size=2, ttl=1)
    cache.set("k1", {"v": 1})
    time.sleep(1.1)
    assert cache.get("k1") is None


# 26-35: More API concurrency and boundary checks
def test_16_api_cache_with_similar_paths():
    r1 = client.get("/path/1")
    r2 = client.get("/path/2")
    assert not r1.json()['metadata']['from_cache']
    assert not r2.json()['metadata']['from_cache']

def test_17_api_cache_key_includes_method():
    r1 = client.get("/path1")
    r2 = client.post("/path1")
    assert not r1.json()['metadata']['from_cache']
    # post endpoint not implemented, expect 405 Method Not Allowed
    assert r2.status_code == 405

def test_18_cache_set_and_get_large_number_of_items():
    cache = CacheTable(max_size=50, ttl=10)
    for i in range(50):
        cache.set(f"k{i}", {"v": i})
    for i in range(50):
        assert cache.get(f"k{i}") is not None

def test_19_cache_eviction_when_full():
    cache = CacheTable(max_size=3, ttl=10)
    cache.set("k1", {"v": 1})
    cache.set("k2", {"v": 2})
    cache.set("k3", {"v": 3})
    cache.get("k1")  # touch k1
    cache.set("k4", {"v": 4})  # evict oldest (k2)
    assert cache.get("k2") is None
    assert cache.get("k1") is not None

def test_20_api_response_structure():
    r = client.get("/somepath")
    data = r.json()
    assert "data" in data and "metadata" in data
    assert "from_cache" in data['metadata']


# 36-50: Tests on error conditions, TTL edge, keys, and concurrency
def test_21_cache_get_nonexistent():
    cache = CacheTable(max_size=2, ttl=10)
    assert cache.get("not_exist") is None

def test_22_cache_eviction_with_same_last_accessed():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"v": 1})
    time.sleep(0.01)
    cache.set("k2", {"v": 2})
    cache.set("k3", {"v": 3})
    # Should evict k1, the least recently accessed
    assert cache.get("k1") is None

def test_23_cache_set_null_value():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", None)
    assert cache.get("k1") is None  # Because value is None

def test_24_api_handle_backend_error(monkeypatch):
    async def fake_get(*args, **kwargs):
        raise Exception("Backend down")

    monkeypatch.setattr("httpx.AsyncClient.get", fake_get)
    response = client.get("/anypath")
    assert response.status_code == 502

def test_25_cache_ttl_very_short():
    cache = CacheTable(max_size=2, ttl=0)
    cache.set("k1", {"v": 1})
    assert cache.get("k1") is None

def test_26_cache_multiple_touch():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"v": 1})
    for _ in range(10):
        cache.touch("k1")
    assert cache.get("k1") is not None

def test_27_api_cache_and_eviction_combined():
    # Clear cache then test eviction via API requests
    # Assuming you can reset cache or restart server for a real env
    pass  # Could be manual or integration test

def test_28_cache_set_same_key_multiple_times():
    cache = CacheTable(max_size=2, ttl=10)
    for i in range(5):
        cache.set("k1", {"v": i})
    assert cache.get("k1") == {"v": 4}

def test_29_cache_eviction_with_edge_cases():
    cache = CacheTable(max_size=1, ttl=10)
    cache.set("k1", {"v": 1})
    cache.set("k2", {"v": 2})
    assert cache.get("k1") is None
    assert cache.get("k2") is not None

def test_30_cache_set_and_get_after_eviction():
    cache = CacheTable(max_size=2, ttl=10)
    cache.set("k1", {"v": 1})
    cache.set("k2", {"v": 2})
    cache.set("k3", {"v": 3})
    assert cache.get("k1") is None
    cache.set("k4", {"v": 4})
    assert cache.get("
