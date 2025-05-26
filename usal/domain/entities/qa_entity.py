from uuid import UUID
from usal.core import BaseEntity
from usal.domain.entities.common_entity import PageEntity


class QAEntity(BaseEntity):
    """
    Entity to represent a question and answer.
    """

    id: UUID
    question: str


class ListQAEntity(BaseEntity):
    """
    Entity to represent a list of question and answers.
    """

    page_info: PageEntity
    records: list[QAEntity]


class ViewQAEntity(QAEntity):
    """
    Entity to represent a view of a question and answer.
    """

    id: UUID
    answer: str


class AdminQAEntity(BaseEntity):
    """
    Entity to represent a question and answer.
    """

    id: UUID
    question: str
    answer: str
    status: str
    type: str


class ListAdminQAEntity(BaseEntity):
    """
    Entity to represent a list of question and answers.
    """

    page_info: PageEntity
    records: list[AdminQAEntity]
