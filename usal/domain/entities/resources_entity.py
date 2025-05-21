from uuid import UUID
from usal.core import BaseEntity


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

    records: list[ResourceEntity]
