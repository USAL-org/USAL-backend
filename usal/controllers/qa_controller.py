from usal.api.schema.request.qa_request import CreateQARequest
from usal.api.schema.response.qa_response import ListQAResponse, QAResponse
from usal.core.api_response import APIResponse, api_response
from usal.api.schema.response.common_response import MessageResponse
from usal.core.enums.qa import QAType
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

    async def list_all_qa(self, type: QAType) -> APIResponse[ListQAResponse]:
        qa_obj = await self.usecase.list_all_qa(type=type)
        return api_response(
            ListQAResponse(
                records=[
                    QAResponse.model_validate(qa, from_attributes=True)
                    for qa in qa_obj.records
                ],
            )
        )
