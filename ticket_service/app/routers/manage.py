from fastapi import APIRouter, status
from fastapi.responses import Response

from enums.responses import RespEnum


router = APIRouter(
    prefix="/manage",
    tags=["Manage"],
)


@router.get(
    "/health/",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses={
        status.HTTP_200_OK: RespEnum.Health.value,
    }
)
async def health():
    return Response(
            status_code=status.HTTP_200_OK
        )
