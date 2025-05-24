from usal.core import BaseEntity


class PageEntity(BaseEntity):
    total_pages: int
    total_records: int
    next: str | None
    previous: str | None
    record_range: list[int]
    current_page: int
    offset: int


class TokenEntity(BaseEntity):
    access_token: str
