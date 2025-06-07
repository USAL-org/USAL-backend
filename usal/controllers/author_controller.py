from usal.api.schema.request.author_request import (
    CreateAuthorRequest,
    FilterAuthorRequest,
)
from usal.api.schema.response.author_response import (
    GetAuthorResponse,
    ListAuthorsResponse,
)
from usal.core.api_response import APIResponse, api_response
from usal.api.schema.response.common_response import MessageResponse
from usal.usecases.author_usecase import AuthorUsecase


class AuthorController:
    def __init__(
        self,
        usecase: AuthorUsecase,
    ) -> None:
        self.usecase = usecase

    async def create_author(
        self,
        request: CreateAuthorRequest,
    ) -> APIResponse[MessageResponse]:
        await self.usecase.create_author(
            request=request,
        )
        return api_response(MessageResponse(message="Author created successfully."))

    async def list_all_author(
        self,
        filter: FilterAuthorRequest,
    ) -> APIResponse[ListAuthorsResponse]:
        author_obj = await self.usecase.list_all_author(filter=filter)
        return api_response(
            ListAuthorsResponse(
                **author_obj.page_info.model_dump(),
                records=[
                    GetAuthorResponse.model_validate(author, from_attributes=True)
                    for author in author_obj.records
                ],
            )
        )
