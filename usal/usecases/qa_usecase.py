from usal.api.schema.request.qa_request import (
    AdminQAFilterRequest,
    CreateQARequest,
    QAFilterRequest,
)
from usal.domain.entities.qa_entity import (
    AdminQAEntity,
    ListAdminQAEntity,
    ListQAEntity,
    QAEntity,
)
from usal.domain.repositories.qa_repo import QARepo


class QAUsecase:
    def __init__(
        self,
        repo: QARepo,
    ) -> None:
        self.repo = repo

    async def create_qa(self, request: CreateQARequest) -> None:
        return await self.repo.create_qa(
            question=request.question,
            answer=request.answer,
            status=request.status,
            type=request.type,
        )

    async def list_all_qa(
        self,
        filter: AdminQAFilterRequest,
    ) -> ListAdminQAEntity:
        qa_obj = await self.repo.list_all_qa(
            page=filter.page,
            limit=filter.limit,
            type=filter.type,
            question=filter.question,
        )
        result = [
            AdminQAEntity.model_validate(author, from_attributes=True)
            for author in qa_obj.records
        ]
        return ListAdminQAEntity(
            page_info=qa_obj.page_info,
            records=result,
        )

    async def list_user_qa(
        self,
        filter: QAFilterRequest,
    ) -> ListQAEntity:
        qa_obj = await self.repo.list_user_qa(
            page=filter.page,
            limit=filter.limit,
            type=filter.type,
            question=filter.question,
        )
        result = [
            QAEntity.model_validate(author, from_attributes=True)
            for author in qa_obj.records
        ]
        return ListQAEntity(
            page_info=qa_obj.page_info,
            records=result,
        )
