from pydantic import Field
from usal.core import BaseRequest
from usal.core.enums.resources import ResourceStatus


class CreateResourcesRequest(BaseRequest):
    """
    Request to create a resource.
    """

    title: str = Field(description="Title of the resource.")
    image: str = Field(description="Image URL of the resource.")
    description: str = Field(description="Description of the resource.")
    file: str = Field(description="File URL of the resource.")
    status: ResourceStatus = Field(
        description="Status of the resource. Can be either 'active' or 'inactive'."
    )


class UpdateResourcesRequest(BaseRequest):
    """
    Request to update a resource.
    """

    title: str | None = Field(None, description="Title of the resource.")
    image: str | None = Field(None, description="Image URL of the resource.")
    description: str | None = Field(None, description="Description of the resource.")
    file: str | None = Field(None, description="File URL of the resource.")
    status: ResourceStatus | None = Field(
        None,
        description="Status of the resource. Can be either 'active' or 'inactive'.",
    )
