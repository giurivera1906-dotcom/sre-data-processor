
import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import redis
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

cache = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)

RESULTS_DIR = Path(__file__).parent / "local-results"
CACHE_TTL_SECONDS = 60


@app.post("/process")
def process():
    try:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({"message": "El cuerpo debe contener JSON válido"}), 400

        canonical = json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        cache_key = "process:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        cached = cache.get(cache_key)
        if cached is not None:
            response = make_response(cached, 200)
            response.headers["Content-Type"] = "application/json"
            response.headers["X-Cache"] = "HIT"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

        result = {
            "input": body,
            "processed": canonical[::-1],
            "request_id": str(uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        now = datetime.now(timezone.utc)
        object_key = f"results/{now:%Y-%m-%d}/{uuid4()}.json"
        destination = RESULTS_DIR / object_key
        destination.parent.mkdir(parents=True, exist_ok=True)

        result["s3_key"] = object_key
        serialized = json.dumps(result, ensure_ascii=False)
        destination.write_text(serialized, encoding="utf-8")

        cache.setex(cache_key, CACHE_TTL_SECONDS, serialized)
        logging.info("cache_miss key=%s object=%s", cache_key, object_key)

        response = make_response(serialized, 200)
        response.headers["Content-Type"] = "application/json"
        response.headers["X-Cache"] = "MISS"
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    except redis.RedisError:
        logging.exception("Redis no está disponible")
        return jsonify({"message": "Redis local no está disponible"}), 500
    except Exception:
        logging.exception("Error procesando solicitud")
        return jsonify({"message": "Error procesando la solicitud local"}), 500


@app.get("/health")
def health():
    cache.ping()
    return jsonify({"status": "ok", "redis": "connected"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
