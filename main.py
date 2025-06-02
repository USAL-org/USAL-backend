import logging
import os
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from usal import controllers, usecases
from usal.api import v1
from usal.api.v1 import routers
from usal.core.exceptions.api_exception import APIError, APIException
from usal.core.injector import Injector, Registrant
from usal.core.permission_checker import AuthorizationError
from usal.domain import repositories as repo_interfaces
from usal.infrastructure import repositories

logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    app = FastAPI(
        debug=True,
        description="USAL Backend API",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "tomorrow-night",
            "tryItOutEnabled": True,
            "persistAuthorization": True,
        },
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4000",
            "http://127.0.0.1:5502",
            "http://localhost:5502",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for route in routers:
        app.include_router(route, prefix="/v1")

    Injector.init(
        app,
        modules=[v1],
        interfaces=[
            Registrant(repo_interfaces, ".+Repo$"),
        ],
        factories=[
            Registrant(controllers, ".+Controller$"),
            Registrant(usecases, ".+Usecase$"),
        ],
        singletons=[
            Registrant(
                repositories,
                ".+Repo$",
            ),
        ],
    )
    return app


app = create_app()


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())


@app.exception_handler(RequestValidationError)
async def request_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        APIError(message=err["msg"], tag=str(err["loc"][-1])) for err in exc.errors()
    ]
    api_exc = APIException(
        message="Request Validation Error!",
        status_code=status.HTTP_400_BAD_REQUEST,
        errors=errors,
    )
    return JSONResponse(status_code=api_exc.status_code, content=api_exc.to_dict())


@app.exception_handler(ResponseValidationError)
async def response_exception_handler(
    request: Request, exc: ResponseValidationError
) -> JSONResponse:
    errors = [
        APIError(message=err["msg"], tag=str(err["loc"][1])) for err in exc.errors()
    ]
    api_exc = APIException(
        message="Response Validation Error!",
        status_code=status.HTTP_400_BAD_REQUEST,
        errors=errors,
    )
    return JSONResponse(status_code=api_exc.status_code, content=api_exc.to_dict())


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(
    request: Request, exc: AuthorizationError
) -> JSONResponse:
    api_exc = APIException(
        message=exc.message,
        status_code=exc.status_code,
    )
    return JSONResponse(status_code=api_exc.status_code, content=api_exc.to_dict())


@app.get("/app")
def read_main(request: Request) -> dict[str, Any]:
    return {
        "backend": "USAL Backend",
        "root_path": request.scope.get("root_path"),
    }


if __name__ == "__main__":
    print(os.getenv("ENV"))
    if os.getenv("ENV") == "local":
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
