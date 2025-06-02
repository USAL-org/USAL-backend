import time
from typing import Set

BLACKLISTED_TOKENS: Set[str] = set()
TOKEN_EXPIRY: dict[str, float] = {}


def add_token_to_blacklist(token: str, remaining_seconds: int) -> None:
    BLACKLISTED_TOKENS.add(token)
    TOKEN_EXPIRY[token] = time.time() + remaining_seconds


def is_token_blacklisted(token: str) -> bool:
    if token not in BLACKLISTED_TOKENS:
        return False

    current_time = time.time()
    if token in TOKEN_EXPIRY and TOKEN_EXPIRY[token] <= current_time:
        BLACKLISTED_TOKENS.discard(token)
        TOKEN_EXPIRY.pop(token, None)
        return False

    return True
