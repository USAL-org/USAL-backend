from typing import Annotated

from fastapi import Depends

from .jwt_bearer import JWTBearer
from .jwt_payload import JWTPayload

Payload = Annotated[JWTPayload, Depends(JWTBearer())]
