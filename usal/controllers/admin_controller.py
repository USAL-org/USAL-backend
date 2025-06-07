from usal.api.schema.request.admin_request import (
    AdminLoginRequest,
)
from usal.api.schema.response.common_response import (
    TokenResponse,
)
from usal.core.api_response import APIResponse, api_response
from usal.usecases.admin_usecase import AdminUsecase


class AdminController:
    def __init__(self, admin_usecase: AdminUsecase) -> None:
        self.usecase = admin_usecase

    async def login(self, request: AdminLoginRequest) -> APIResponse[TokenResponse]:
        token = await self.usecase.login(
            username=request.username,
            password=request.password.get_secret_value(),
        )

        return api_response(TokenResponse.model_validate(token, from_attributes=True))
