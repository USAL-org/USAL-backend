from uuid import UUID
from usal.core import BaseSchema


class ResourceResponse(BaseSchema):
    """
    Response to get a resource.
    """

    id: UUID
    title: str
    image: str
    description: str
    file: str


class ListResourcesResponse(BaseSchema):
    """
    Response to list resources.
    """

    records: list[ResourceResponse]
