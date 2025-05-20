from pydantic import Field
from usal.core import BaseRequest
from usal.core.enums.qa import QAStatus, QAType


class CreateQARequest(BaseRequest):
    """
    Request to create a Q&A.
    """

    question: str = Field(description="Question of the Q&A.")
    answer: str = Field(description="Answer of the Q&A.")
    status: QAStatus = Field(
        description="Status of the Q&A. Can be either 'active' or 'inactive'."
    )
    type: QAType = Field(description="Type of the Q&A.")


class UpdateQARequest(BaseRequest):
    """
    Request to update a Q&A.
    """

    question: str | None = Field(None, description="Question of the Q&A.")
    answer: str | None = Field(None, description="Answer of the Q&A.")
    status: QAStatus | None = Field(
        None,
        description="Status of the Q&A. Can be either 'active' or 'inactive'.",
    )
    type: QAType | None = Field(None, description="Type of the Q&A.")
