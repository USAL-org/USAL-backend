from usal.api.schema.request.resources_request import (
    AdminFilterResourcesRequest,
    CreateResourcesRequest,
    FilterResourcesRequest,
)
from usal.domain.entities.resources_entity import (
    AdminResourceEntity,
    ListAdminResourceEntity,
    ListResourceEntity,
    ResourceEntity,
)
from usal.domain.repositories.resources_repo import ResourcesRepo


class ResourcesUsecase:
    def __init__(
        self,
        repo: ResourcesRepo,
    ) -> None:
        self.repo = repo

    async def create_resources(self, request: CreateResourcesRequest) -> None:
        return await self.repo.create_resource(
            title=request.title,
            image=request.image,
            description=request.description,
            file=request.file,
            status=request.status,
        )

    async def list_all_resources(
        self,
        filter: AdminFilterResourcesRequest,
    ) -> ListAdminResourceEntity:
        resource_obj = await self.repo.list_all_resources(
            page=filter.page,
            limit=filter.limit,
            search=filter.search,
        )
        result = [
            AdminResourceEntity.model_validate(resource, from_attributes=True)
            for resource in resource_obj.records
        ]
        return ListAdminResourceEntity(
            page_info=resource_obj.page_info,
            records=result,
        )

    async def list_user_resources(
        self,
        filter: FilterResourcesRequest,
    ) -> ListResourceEntity:
        resource_obj = await self.repo.list_user_resources(
            page=filter.page,
            limit=filter.limit,
            search=filter.search,
        )
        result = [
            ResourceEntity.model_validate(resource, from_attributes=True)
            for resource in resource_obj.records
        ]
        return ListResourceEntity(
            page_info=resource_obj.page_info,
            records=result,
        )
