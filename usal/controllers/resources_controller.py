from usal.api.schema.request.resources_request import (
    AdminFilterResourcesRequest,
    CreateResourcesRequest,
    FilterResourcesRequest,
)
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.resources_response import (
    AdminResourceResponse,
    ListAdminResourcesResponse,
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
        filter: AdminFilterResourcesRequest,
    ) -> APIResponse[ListAdminResourcesResponse]:
        resources_obj = await self.usecase.list_all_resources(filter)
        return api_response(
            ListAdminResourcesResponse(
                **resources_obj.page_info.model_dump(),
                records=[
                    AdminResourceResponse.model_validate(
                        resources, from_attributes=True
                    )
                    for resources in resources_obj.records
                ],
            )
        )

    async def list_user_resources(
        self,
        filter: FilterResourcesRequest,
    ) -> APIResponse[ListResourcesResponse]:
        resources_obj = await self.usecase.list_user_resources(filter)
        return api_response(
            ListResourcesResponse(
                **resources_obj.page_info.model_dump(),
                records=[
                    ResourceResponse.model_validate(resources, from_attributes=True)
                    for resources in resources_obj.records
                ],
            )
        )
