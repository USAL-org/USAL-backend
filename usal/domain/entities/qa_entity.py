from uuid import UUID
from usal.core import BaseEntity


class QAEntity(BaseEntity):
    """
    Entity to represent a question and answer.
    """

    id: UUID
    question: str
    answer: str


class ListQAEntity(BaseEntity):
    """
    Entity to represent a list of question and answers.
    """

    records: list[QAEntity]
