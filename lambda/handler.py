
import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from uuid import uuid4

import boto3
import redis

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ["S3_BUCKET"]
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
CACHE_TTL_SECONDS = 60

# LocalStack is used only when an endpoint is explicitly configured.
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
s3_options = {}
if S3_ENDPOINT_URL:
    s3_options["endpoint_url"] = S3_ENDPOINT_URL

s3 = boto3.client("s3", **s3_options)

cache = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


def response(status_code, payload, cache_status):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "X-Cache": cache_status,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
        },
        "body": json.dumps(payload, ensure_ascii=False),
    }


def lambda_handler(event, context):
    try:
        
        if not isinstance(event, dict):
            return response(
                400,
                {"message": "Request event must be a JSON object."},
                "MISS",
            )

        if "body" not in event:
            body = event
        else:
            raw_body = event["body"]

            if raw_body is None or raw_body == "":
                body = {}
            elif isinstance(raw_body, str):
                try:
                    body = json.loads(raw_body)
                except json.JSONDecodeError:
                    return response(
                        400,
                        {"message": "Request body is not valid JSON."},
                        "MISS",
                    )
            else:
                body = raw_body

        if not isinstance(body, dict):
            return response(
                400,
                {"message": "Request body must be a JSON object."},
                "MISS",
            )


        canonical = json.dumps(
            body,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        cache_key = "process:" + hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

        cached = cache.get(cache_key)
        if cached is not None:
            logger.info("cache_hit key=%s", cache_key)
            return response(200, json.loads(cached), "HIT")

        result = {
            "input": body,
            "processed": canonical[::-1],
            "request_id": getattr(context, "aws_request_id", str(uuid4())),
        }

        now = datetime.now(timezone.utc)
        object_key = f"results/{now:%Y-%m-%d}/{uuid4()}.json"
        result["s3_key"] = object_key

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=object_key,
            Body=json.dumps(result, ensure_ascii=False).encode("utf-8"),
            ContentType="application/json",
        )

        cache.setex(
            cache_key,
            CACHE_TTL_SECONDS,
            json.dumps(result, ensure_ascii=False),
        )

        logger.info("cache_miss key=%s s3_key=%s", cache_key, object_key)
        return response(200, result, "MISS")

    except Exception:
        logger.exception("Request processing failed")
        return response(
            500,
            {
                "message": (
                    "Error processing the request; "
                    "check the application logs."
                )
            },
            "MISS",
        )
