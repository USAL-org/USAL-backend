from uuid import UUID
from usal.api.schema.request.qa_request import (
    AdminQAFilterRequest,
    CreateQARequest,
    QAFilterRequest,
)
from usal.api.schema.response.qa_response import (
    AdminQAResponse,
    ListAdminQAResponse,
    ListQAResponse,
    QAResponse,
    ViewQAResponse,
)
from usal.core.api_response import APIResponse, api_response
from usal.api.schema.response.common_response import MessageResponse
from usal.usecases.qa_usecase import QAUsecase


class QAController:
    def __init__(
        self,
        usecase: QAUsecase,
    ) -> None:
        self.usecase = usecase

    async def create_qa(
        self,
        request: CreateQARequest,
    ) -> APIResponse[MessageResponse]:
        await self.usecase.create_qa(
            request=request,
        )
        return api_response(MessageResponse(message="QA created successfully."))

    async def list_all_qa(
        self, filter: AdminQAFilterRequest
    ) -> APIResponse[ListAdminQAResponse]:
        qa_obj = await self.usecase.list_all_qa(filter)
        return api_response(
            ListAdminQAResponse(
                **qa_obj.page_info.model_dump(),
                records=[
                    AdminQAResponse.model_validate(qa, from_attributes=True)
                    for qa in qa_obj.records
                ],
            )
        )

    async def list_user_qa(
        self, filter: QAFilterRequest
    ) -> APIResponse[ListQAResponse]:
        qa_obj = await self.usecase.list_user_qa(filter)
        return api_response(
            ListQAResponse(
                **qa_obj.page_info.model_dump(),
                records=[
                    QAResponse.model_validate(qa, from_attributes=True)
                    for qa in qa_obj.records
                ],
            )
        )

    async def get_qa_by_id(
        self,
        qa_id: UUID,
    ) -> APIResponse[ViewQAResponse]:
        qa_obj = await self.usecase.get_qa_by_id(qa_id=qa_id)
        return api_response(
            ViewQAResponse.model_validate(
                qa_obj,
                from_attributes=True,
            )
        )
