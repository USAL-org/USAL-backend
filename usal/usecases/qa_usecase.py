from usal.api.schema.request.qa_request import CreateQARequest
from usal.core.enums.qa import QAType
from usal.domain.entities.qa_entity import ListQAEntity
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
        type: QAType,
    ) -> ListQAEntity:
        return await self.repo.list_qa(
            type=type,
        )
