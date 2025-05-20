from pydantic import Field

from usal.core import BaseRequest


class PaginationRequest(BaseRequest):
    page: int = Field(1, ge=1, description="The page number for the pagination.")
    limit: int = Field(10, description="The number of result you want in a query.")
