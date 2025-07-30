# 🚀 LiteCDN: A Lightweight Caching Layer for Fast and Efficient Content Delivery

![LiteCDN Architecture](figure/figure.png)

**LiteCDN** is a lightweight, extensible caching system that emulates core CDN functionality. It supports time-to-live (TTL)-based expiration, least recently used (LRU) eviction, and a RESTful HTTP API for seamless cache interaction. Designed for both educational purposes and practical application, LiteCDN is ideal for rapid prototyping, system simulation, or integration into microservice architectures.

---

## 📌 Key Features

- **TTL-Based Expiration** — Automatically invalidates cache entries based on configurable timeouts.
- **LRU Eviction Policy** — Removes the least recently used entries when the cache reaches its capacity.
- **HTTP-Aware Caching** — Differentiates entries by HTTP method and request path to prevent collisions.
- **RESTful API Interface** — Built with FastAPI, providing endpoints for managing cache operations and diagnostics.
- **Simulated Origin Server** — Includes a mock backend to replicate real-world HTTP response behavior.
- **Test Coverage** — Includes comprehensive `pytest`-based tests to ensure reliability and correctness.
- **Modular Design** — Clean separation of core caching logic and API layers for easy customization and extension.

---

## 🗂️ Project Structure

```bash
.
├── app.py             # FastAPI server exposing cache API endpoints
├── cache.py           # Core cache logic (TTL, LRU, key management)
├── main_server.py     # Simulated backend origin server for testing
├── test.py            # Unit tests for cache functionality and API
├── test.sh            # Shell script for running tests
├── requirements.txt   # Project dependencies
└── figure/            # Diagrams and visuals
```

---

## ⚙️ Setup & Installation

1. **Create and activate** a Python 3.9+ virtual environment (recommended):

   ```bash
   python3 -m venv env
   source env/bin/activate   # macOS/Linux
   .\env\Scripts\activate    # Windows

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
## 🚀 Running the Application
Launch the FastAPI app locally with hot reload support:

```bash
uvicorn main_server:server --port 8000
uvicorn app:app --port 8080
````
---
## 🧪 Running Tests
```bash
pytest test.py -v
./test.sh
````
---
## 📌 Key Features
- **TTL Cache:** Automatically expires cache entries after a configurable duration.
- **LRU Eviction:** When capacity is full, least recently used items are removed.
- **Multi-Method Support:** Cache keys include HTTP method to avoid collisions.
- **API Metadata:** Responses include cache hit status and cache keys for transparency.
- **Test-Driven:** Comprehensive automated tests to maintain code quality.
- **Modular Design:** Easily extend cache policies or API features.

---

If you want, I can also help add:

- Status badges (e.g., build, coverage)
- Example API documentation with sample requests/responses
- Docker support or deployment instructions

Just let me know!







