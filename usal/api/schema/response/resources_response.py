from uuid import UUID
from usal.core import BaseSchema, PaginatedSchema
from usal.core.enums.resources import ResourceStatus


class ResourceResponse(BaseSchema):
    """
    Response to get a resource.
    """

    id: UUID
    title: str
    image: str
    description: str
    file: str


class ListResourcesResponse(PaginatedSchema):
    """
    Response to list resources.
    """

    records: list[ResourceResponse]


class AdminResourceResponse(BaseSchema):
    """
    Response to get a resource.
    """

    id: UUID
    title: str
    image: str
    description: str
    file: str
    status: ResourceStatus


class ListAdminResourcesResponse(PaginatedSchema):
    """
    Response to list resources.
    """

    records: list[AdminResourceResponse]
