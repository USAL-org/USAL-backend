from abc import abstractmethod
# from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.core.enums.resources import ResourceStatus
from usal.domain.entities.resources_entity import (
    ListAdminResourceEntity,
    ListResourceEntity,
)


class ResourcesRepo(DbRepo):
    @abstractmethod
    async def create_resource(
        self,
        title: str,
        image: str,
        description: str,
        file: str,
        status: ResourceStatus,
    ) -> None:
        """
        Create a resource.

        Parameters:
            title (str): Title of the resource.
            image (str): Image of the resource.
            description (str): Description of the resource.
            file (str): File of the resource.
            status (ResourceStatus): Status of the resource.

        Returns:
            None
        """

    # @abstractmethod
    # async def update_resource(
    #     self,
    #     resource_id: str,
    #     title: str | None = None,
    #     image: str | None = None,
    #     description: str | None = None,
    #     file: str | None = None,
    #     status: ResourceStatus | None = None,
    # ) -> None:
    #     """
    #     Update a resource.

    #     Parameters:
    #         resource_id (str): ID of the resource.
    #         title (str | None): Title of the resource.
    #         image (str | None): Image of the resource.
    #         description (str | None): Description of the resource.
    #         file (str | None): File of the resource.
    #         status (ResourceStatus | None): Status of the resource.

    #     Returns:
    #         None
    #     """

    @abstractmethod
    async def list_all_resources(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> ListAdminResourceEntity:
        """
        List resources.

        Parameters:
            page (int): Page number.
            limit (int): Number of items per page.
            search (str | None): Search term.
            status (ResourceStatus | None): Status of the resource.

        Returns:
            ListResourceEntity: List of resources.
        """

    @abstractmethod
    async def list_user_resources(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> ListResourceEntity:
        """
        List resources.

        Parameters:
            page (int): Page number.
            limit (int): Number of items per page.
            search (str | None): Search term.

        Returns:
            ListResourceEntity: List of resources.
        """
