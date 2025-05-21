from typing import override

from usal.core.enums.qa import QAStatus, QAType
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.qa_entity import ListQAEntity, QAEntity
from usal.domain.repositories.qa_repo import QARepo
from usal.infrastructure.queries.qa import create_qa_async_edgeql, list_qa_async_edgeql


class DbQARepo(QARepo):
    @override
    async def create_qa(
        self,
        question: str,
        answer: str,
        status: QAStatus,
        type: QAType,
    ) -> None:
        async with self.session() as session:
            qa_obj = await create_qa_async_edgeql.create_qa(
                session,
                question=question,
                answer=answer,
                status=status,
                type=type,
            )
            if not qa_obj:
                raise api_exception(
                    message="Unable to create Q&A. Please try again.",
                )

    @override
    async def list_qa(self, type: QAType) -> ListQAEntity:
        async with self.session() as session:
            db_qa = await list_qa_async_edgeql.list_qa(
                session,
                type=type,
            )
            return ListQAEntity(
                records=[
                    QAEntity.model_validate(qa, from_attributes=True) for qa in db_qa
                ]
            )
