from abc import abstractmethod
from uuid import UUID
# from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.core.enums.qa import QAStatus, QAType
from usal.domain.entities.qa_entity import ListAdminQAEntity, ListQAEntity, ViewQAEntity


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
    async def list_all_qa(
        self,
        page: int,
        limit: int,
        type: QAType | None = None,
        question: str | None = None,
    ) -> ListAdminQAEntity:
        """
        List all question and answers.

        Parameters:
            page (int): Page number.
            limit (int): Number of records per page.
            question (str | None): Question to filter by.
            type (QAType | None): Type of the question and answer.

        Returns:
            ListQAEntity: List of question and answers.
        """

    @abstractmethod
    async def list_user_qa(
        self,
        page: int,
        limit: int,
        type: QAType,
        question: str | None = None,
    ) -> ListQAEntity:
        """
        List all question and answers.

        Parameters:
            page (int): Page number.
            limit (int): Number of records per page.
            question (str | None): Question to filter by.
            type (QAType | None): Type of the question and answer.
            status (QAStatus | None): Status of the question and answer.

        Returns:
            ListAdminQAEntity: List of question and answers.
        """

    @abstractmethod
    async def get_qa_by_id(
        self,
        qa_id: UUID,
    ) -> ViewQAEntity:
        """
        Get a question and answer by ID.

        Parameters:
            qa_id (UUID): ID of the question and answer.

        Returns:
            ViewQAEntity: Question and answer.
        """
