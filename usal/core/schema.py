from pydantic import BaseModel

BaseSchema = BaseModel


class PaginationSchema(BaseSchema):
    total_pages: int
    total_records: int
    next: str | None
    previous: str | None
    record_range: list[int]
    current_page: int
