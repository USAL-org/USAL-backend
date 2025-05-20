from typing import override

from usal.core.enums.resources import ResourceStatus
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.resources_entity import ListResourceEntity, ResourceEntity
from usal.domain.repositories.resources_repo import ResourcesRepo
from usal.infrastructure.queries.resources import (
    create_resources_async_edgeql,
    list_resources_async_edgeql,
)


class DbResourcesRepo(ResourcesRepo):
    @override
    async def create_resource(
        self,
        title: str,
        image: str,
        description: str,
        file: str,
        status: ResourceStatus,
    ) -> None:
        async with self.session() as session:
            resource_obj = await create_resources_async_edgeql.create_resources(
                session,
                title=title,
                image=image,
                description=description,
                file=file,
                status=status,
            )
            if not resource_obj:
                raise api_exception(
                    message="Unable to create resource. Please try again.",
                )

    @override
    async def list_resources(self) -> ListResourceEntity:
        async with self.session() as session:
            db_resources = await list_resources_async_edgeql.list_resources(session)
            return ListResourceEntity(
                records=[
                    ResourceEntity.model_validate(resource, from_attributes=True)
                    for resource in db_resources
                ],
            )
