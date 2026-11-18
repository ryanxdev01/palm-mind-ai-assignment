
import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6380/0"
)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)

CHAT_HISTORY_TTL = 86400  # 24 hours


def check_redis_connection() -> bool:
    """Check whether Redis is available."""
    return redis_client.ping()


def save_chat_message(
    session_id: str,
    role: str,
    content: str
) -> None:
    """Save one conversation message in Redis."""

    key = f"chat:{session_id}"

    message = {
        "role": role,
        "content": content
    }

    redis_client.rpush(key, json.dumps(message))
    redis_client.expire(key, CHAT_HISTORY_TTL)


def get_chat_history(session_id: str) -> list[dict]:
    """Retrieve conversation history from Redis."""

    key = f"chat:{session_id}"

    messages = redis_client.lrange(key, 0, -1)

    return [
        json.loads(message)
        for message in messages
    ]
