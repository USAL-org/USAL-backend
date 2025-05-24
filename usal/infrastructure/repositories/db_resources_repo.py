from typing import override

from usal.core.enums.resources import ResourceStatus
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.resources_entity import (
    AdminResourceEntity,
    ListAdminResourceEntity,
    ListResourceEntity,
    ResourceEntity,
)
from usal.domain.repositories.resources_repo import ResourcesRepo
from usal.infrastructure.queries.resources import (
    create_resources_async_edgeql,
    get_all_resources_count_async_edgeql,
    get_user_resources_count_async_edgeql,
    list_resources_async_edgeql,
    list_user_resources_async_edgeql,
)
from usal.infrastructure.repositories.pagination_repo import paginate


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
    async def list_all_resources(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> ListAdminResourceEntity:
        async with self.session() as session:
            total_count = (
                await get_all_resources_count_async_edgeql.get_all_resources_count(
                    session,
                    search=search,
                )
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_resource = await list_resources_async_edgeql.list_resources(
                session,
                offset=page_info.offset,
                limit=limit,
                search=search,
            )
            return ListAdminResourceEntity(
                page_info=page_info,
                records=[
                    AdminResourceEntity.model_validate(resource, from_attributes=True)
                    for resource in db_resource
                ],
            )

    @override
    async def list_user_resources(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> ListResourceEntity:
        async with self.session() as session:
            total_count = (
                await get_user_resources_count_async_edgeql.get_user_resources_count(
                    session,
                    search=search,
                )
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_resource = await list_user_resources_async_edgeql.list_user_resources(
                session,
                offset=page_info.offset,
                limit=limit,
                search=search,
            )
            return ListResourceEntity(
                page_info=page_info,
                records=[
                    ResourceEntity.model_validate(resource, from_attributes=True)
                    for resource in db_resource
                ],
            )
