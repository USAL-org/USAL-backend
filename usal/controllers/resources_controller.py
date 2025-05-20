from usal.api.schema.request.resources_request import CreateResourcesRequest
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.resources_response import (
    ListResourcesResponse,
    ResourceResponse,
)
from usal.core.api_response import APIResponse, api_response
from usal.usecases.resources_usecase import ResourcesUsecase


class ResourcesController:
    def __init__(
        self,
        usecase: ResourcesUsecase,
    ) -> None:
        self.usecase = usecase

    async def create_resources(
        self,
        request: CreateResourcesRequest,
    ) -> APIResponse[MessageResponse]:
        await self.usecase.create_resources(
            request=request,
        )
        return api_response(MessageResponse(message="Resource created successfully."))

    async def list_all_resources(
        self,
    ) -> APIResponse[ListResourcesResponse]:
        resources_obj = await self.usecase.list_all_resources()
        return api_response(
            ListResourcesResponse(
                records=[
                    ResourceResponse.model_validate(resources, from_attributes=True)
                    for resources in resources_obj.records
                ],
            )
        )
