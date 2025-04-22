import hashlib
import random
import string
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from nilva_session.settings import DEFAULT


def random_token_generator(size: int = 6, chars: list = string.ascii_lowercase + string.digits) -> str:
    return "".join(random.choices(chars, k=size))


def token_generator():
    try:
        token_size = getattr(settings, "USER_SESSION", {}).get("TOKEN_SIZE", DEFAULT["TOKEN_SIZE"])
        user_session_size = max(int(token_size), 50)
    except ValueError:
        raise ValueError("Invalid token size in settings, reverting to default size.")

    return random_token_generator(size=user_session_size)


def token_expire_at_generator():
    user_session_expire_at = getattr(settings, "USER_SESSION", {}).get("EXPIRE_AT", DEFAULT["EXPIRE_AT"])
    if not isinstance(user_session_expire_at, timedelta):
        raise ValueError("Invalid expiration time in settings.")

    return timezone.now() + user_session_expire_at


def hash_data(data: str):
    if isinstance(data, str):
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
    return ""
