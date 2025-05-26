from uuid import UUID
from usal.core import BaseSchema, PaginatedSchema
from usal.core.enums.qa import QAStatus, QAType


class QAResponse(BaseSchema):
    """
    Response to get a question and answer.
    """

    id: UUID
    question: str


class ListQAResponse(PaginatedSchema):
    """
    Response to list question and answers.
    """

    records: list[QAResponse]


class ViewQAResponse(QAResponse):
    """
    Response to view a question and answer.
    """

    id: UUID
    answer: str


class AdminQAResponse(BaseSchema):
    """
    Response to get a question and answer.
    """

    id: UUID
    question: str
    answer: str
    status: QAStatus
    type: QAType


class ListAdminQAResponse(PaginatedSchema):
    """
    Response to list question and answers.
    """

    records: list[AdminQAResponse]
