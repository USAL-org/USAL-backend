from usal.api.schema.request.resources_request import CreateResourcesRequest
from usal.domain.entities.resources_entity import ListResourceEntity
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

    async def list_all_resources(self) -> ListResourceEntity:
        return await self.repo.list_resources()
