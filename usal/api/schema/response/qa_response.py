from uuid import UUID
from usal.core import BaseSchema


class QAResponse(BaseSchema):
    """
    Response to get a question and answer.
    """

    id: UUID
    question: str
    answer: str


class ListQAResponse(BaseSchema):
    """
    Response to list question and answers.
    """

    records: list[QAResponse]
