from uuid import UUID
from usal.core import BaseEntity
from usal.domain.entities.common_entity import PageEntity


class ResourceEntity(BaseEntity):
    """
    Entity to represent a resource.
    """

    id: UUID
    title: str
    image: str
    description: str
    file: str


class ListResourceEntity(BaseEntity):
    """
    Entity to represent a list of resources.
    """

    page_info: PageEntity
    records: list[ResourceEntity]


class AdminResourceEntity(BaseEntity):
    """
    Entity to represent a resource.
    """

    id: UUID
    title: str
    image: str
    description: str
    file: str
    status: str


class ListAdminResourceEntity(BaseEntity):
    """
    Entity to represent a list of resources.
    """

    page_info: PageEntity
    records: list[AdminResourceEntity]
