from datetime import datetime, timedelta, timezone
from secrets import choice
from string import digits

OTP_LENGTH = 6
OTP_EXPIRE_MINUTES = 5


def generate_random_digits(length: int = OTP_LENGTH) -> str:
    characters = digits
    return "".join(choice(characters) for _ in range(length))


def calculate_expiration_time(minutes: int = OTP_EXPIRE_MINUTES) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)
