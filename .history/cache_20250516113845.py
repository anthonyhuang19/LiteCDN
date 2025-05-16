'''
Making temporary cache .
'''
import time
from typing import Dict, Optional

class CacheTable:
    def __init__(self, max_size: int = 100, ttl: int = 300):
        self.cache: Dict[str, dict] = {}
        self.max_size = max_size
        self.ttl = ttl  # Time To Live in seconds

    def get(self, key: str) -> Optional[dict]:
        """Check cache and update last_accessed if found"""
        if key not in self.cache:
            return None
            
        item = self.cache[key]
        if time.time() - item['created_at'] > self.ttl:
            del self.cache[key]
            return None
            
        # "Touch" the item by updating last_accessed
        self.touch(key)
        return item['value']

    def touch(self, key: str) -> None:
        """Update last_accessed without changing value"""
        if key in self.cache:
            self.cache[key]['last_accessed'] = time.time()

    def set(self, key: str, value: dict) -> None:
        """Add item with eviction if cache is full"""
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
            
        self.cache[key] = {
            'value': value,
            'created_at': time.time(),
            'last_accessed': time.time()
        }

    def _evict_oldest(self) -> None:
        """Evict least recently accessed item"""
        oldest_key = min(self.cache.keys(), 
                        key=lambda k: self.cache[k]['last_accessed'])
        del self.cache[oldest_key]
        print(f"Evicted {oldest_key} from cache")

    def print_cache(self) -> None:
        """Debug method to see cache contents"""
        print("\n--- Cache Contents ---")
        for key, item in self.cache.items():
            age = time.time() - item['created_at']
            last_access = time.time() - item['last_accessed']
            print(f"{key}:")
            print(f"  Value: {item['value']}")
            print(f"  Age: {age:.1f}s")
            print(f"  Last accessed: {last_access:.1f}s ago")