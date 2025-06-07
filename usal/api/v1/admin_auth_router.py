from typing import Annotated

from fastapi import APIRouter
from wireup import Inject

from usal.api.schema.request.admin_request import AdminLoginRequest
from usal.api.schema.response.common_response import TokenResponse
from usal.controllers.admin_controller import AdminController
from usal.core.api_response import APIResponse

AdminAuthRouter = APIRouter(
    tags=["Admin Auth"],
    prefix="/admin-auth",
)


@AdminAuthRouter.post("/login")
async def login(
    controller: Annotated[AdminController, Inject()],
    request: AdminLoginRequest,
) -> APIResponse[TokenResponse]:
    return await controller.login(request)
