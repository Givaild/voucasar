import os
import time
from collections import deque
from threading import Lock
from fastapi import HTTPException, Request, status

_LIMITERS: dict[str, deque] = {}
_LOCK = Lock()


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def enforce_rate_limit(request: Request, key: str, limit: int, window_seconds: int) -> None:
    now = time.time()
    client_ip = _get_client_ip(request)
    bucket_key = f"{key}:{client_ip}"

    with _LOCK:
        bucket = _LIMITERS.get(bucket_key)
        if bucket is None:
            bucket = deque()
            _LIMITERS[bucket_key] = bucket

        cutoff = now - window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()

        if len(bucket) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Muitas requisicoes. Tente novamente em alguns instantes.",
                headers={"Retry-After": str(window_seconds)},
            )

        bucket.append(now)


def get_limit_from_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default
