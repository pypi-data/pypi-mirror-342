from datetime import timedelta

DEFAULT = {
    "TOKEN_SIZE": 10,
    "EXPIRE_AT": timedelta(days=1),
    "SESSION_CACHE_PREFIX": "user_session:",
    "SESSION_ID_CACHE_PREFIX": "user_session_by_id:",
    "SESSION_CACHE_TTL": 60 * 60,  # 1hour,
    "SESSION_ID_CLAIM": "session_id",
}
