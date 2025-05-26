from typing import override
from uuid import UUID

from usal.core.enums.qa import QAStatus, QAType
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.qa_entity import (
    AdminQAEntity,
    ListAdminQAEntity,
    ListQAEntity,
    QAEntity,
    ViewQAEntity,
)
from usal.domain.repositories.qa_repo import QARepo
from usal.infrastructure.queries.qa import (
    create_qa_async_edgeql,
    get_all_qa_count_async_edgeql,
    get_qa_by_id_async_edgeql,
    get_user_qa_count_async_edgeql,
    list_qa_async_edgeql,
    list_user_qa_async_edgeql,
)
from usal.infrastructure.repositories.pagination_repo import paginate


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

    # @override
    # async def list_qa(self, type: QAType) -> ListQAEntity:
    #     async with self.session() as session:
    #         db_qa = await list_qa_async_edgeql.list_qa(
    #             session,
    #             type=type,
    #         )
    #         return ListQAEntity(
    #             records=[
    #                 QAEntity.model_validate(qa, from_attributes=True) for qa in db_qa
    #             ]
    #         )
    @override
    async def list_all_qa(
        self,
        page: int,
        limit: int,
        type: QAType | None = None,
        question: str | None = None,
    ) -> ListAdminQAEntity:
        async with self.session() as session:
            total_count = await get_all_qa_count_async_edgeql.get_all_qa_count(
                session,
                type=type,
                question=question,
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_qa = await list_qa_async_edgeql.list_qa(
                session,
                offset=page_info.offset,
                limit=limit,
                question=question,
                type=type,
            )
            return ListAdminQAEntity(
                page_info=page_info,
                records=[
                    AdminQAEntity.model_validate(qa, from_attributes=True)
                    for qa in db_qa
                ],
            )

    @override
    async def list_user_qa(
        self,
        page: int,
        limit: int,
        type: QAType,
        question: str | None = None,
    ) -> ListQAEntity:
        async with self.session() as session:
            total_count = await get_user_qa_count_async_edgeql.get_user_qa_count(
                session,
                type=type,
                question=question,
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_qa = await list_user_qa_async_edgeql.list_user_qa(
                session,
                offset=page_info.offset,
                limit=limit,
                question=question,
                type=type,
            )
            return ListQAEntity(
                page_info=page_info,
                records=[
                    QAEntity.model_validate(qa, from_attributes=True) for qa in db_qa
                ],
            )

    @override
    async def get_qa_by_id(self, qa_id: UUID) -> ViewQAEntity:
        async with self.session() as session:
            db_qa = await get_qa_by_id_async_edgeql.get_qa_by_id(
                session,
                qa_id=qa_id,
            )
            if not db_qa:
                raise api_exception(
                    message="QA not found.",
                )
            return ViewQAEntity.model_validate(db_qa, from_attributes=True)
