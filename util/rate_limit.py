import os
import time
from collections import deque
from threading import Lock
from fastapi import HTTPException, Request, status

_LIMITERS: dict[str, deque] = {}
_LOCK = Lock()


def _get_client_ip(request: Request) -> str:
    """
    Obtém o IP real do cliente.
    Só confia em X-Forwarded-For se o IP direto for de uma rede privada
    (ou seja, um proxy/load-balancer confiável, não o cliente final).
    Isso evita que clientes injetem um X-Forwarded-For falso para burlar o rate limit.
    """
    direct_ip = request.client.host if request.client else None

    # Detecta se o IP direto é de uma rede privada/confiável (proxy/nginx)
    def _is_private(ip: str) -> bool:
        return (
            ip.startswith("10.") or
            ip.startswith("172.") or
            ip.startswith("192.168.") or
            ip in ("127.0.0.1", "::1", "localhost")
        )

    if direct_ip and _is_private(direct_ip):
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()

    return direct_ip or "unknown"


def _consume(bucket_key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
    """
    Tenta consumir 1 slot do bucket. Retorna (permitido, retry_after).
    Se permitido for False, retry_after indica em quantos segundos o cliente
    pode tentar de novo (1 segundo, no mínimo).
    """
    now = time.time()
    with _LOCK:
        bucket = _LIMITERS.get(bucket_key)
        if bucket is None:
            bucket = deque()
            _LIMITERS[bucket_key] = bucket

        cutoff = now - window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()

        if len(bucket) >= limit:
            # Retry-After: tempo até o item mais antigo sair da janela
            retry_after = max(1, int(bucket[0] + window_seconds - now) + 1)
            return False, retry_after

        bucket.append(now)
        return True, 0


def enforce_rate_limit(request: Request, key: str, limit: int, window_seconds: int) -> None:
    """
    Aplica rate limiting por IP usando uma chave customizável.
    Lança HTTPException 429 quando o limite é atingido.
    """
    client_ip = _get_client_ip(request)
    bucket_key = f"{key}:{client_ip}"
    allowed, retry_after = _consume(bucket_key, limit, window_seconds)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas requisicoes. Tente novamente em alguns instantes.",
            headers={"Retry-After": str(retry_after)},
        )


def check_rate_limit(request: Request, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
    """
    Mesma lógica de enforce_rate_limit, mas retorna (permitido, retry_after)
    em vez de lançar exceção. Útil para middlewares.
    """
    client_ip = _get_client_ip(request)
    bucket_key = f"{key}:{client_ip}"
    return _consume(bucket_key, limit, window_seconds)


def get_limit_from_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def get_excluded_paths_from_env(name: str) -> set[str]:
    """
    Lê uma variável de ambiente com paths separados por vírgula e retorna
    um set com os paths limpos. Usado para excluir endpoints do rate limiting
    global (ex.: /health, /docs).
    """
    raw = os.getenv(name, "")
    if not raw:
        return set()
    return {p.strip() for p in raw.split(",") if p.strip()}
