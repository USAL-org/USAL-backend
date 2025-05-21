from abc import abstractmethod
# from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.core.enums.qa import QAStatus, QAType
from usal.domain.entities.qa_entity import ListQAEntity


class QARepo(DbRepo):
    @abstractmethod
    async def create_qa(
        self,
        question: str,
        answer: str,
        status: QAStatus,
        type: QAType,
    ) -> None:
        """
        Create a question and answer.

        Parameters:
            question (str): Question.
            answer (str): Answer.
            status (QAStatus): Status of the question and answer.
            type (QAType): Type of the question and answer.

        Returns:
            None
        """

    # @abstractmethod
    # async def update_qa(
    #     self,
    #     qa_id: UUID,
    #     question: str | None = None,
    #     answer: str | None = None,
    #     status: QAStatus | None = None,
    #     type: QAType | None = None,
    # ) -> None:
    #     """
    #     Update a question and answer.

    #     Parameters:
    #         qa_id (str): ID of the question and answer.
    #         question (str | None): Question.
    #         answer (str | None): Answer.
    #         status (QAStatus | None): Status of the question and answer.
    #         type (QAType | None): Type of the question and answer.
    #     Returns:
    #         None
    #     """

    @abstractmethod
    async def list_qa(self, type: QAType) -> ListQAEntity:
        """
        List question and answers.

        Parameters:
            type (QAType): Type of the question and answer.

        Returns:
            ListQAEntity: List of question and answers.
        """
