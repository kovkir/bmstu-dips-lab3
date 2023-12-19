from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Annotated

from schemas.airport import AirportCreate, Airport
from services.airport import AirportService
from enums.responses import RespAirportEnum
from utils.database import get_db
from cruds.interfaces.airport import IAirportCRUD
from cruds.airport import AirportCRUD
# from cruds.mocks.airport import AirportMockCRUD


def get_airport_crud() -> type[IAirportCRUD]:
    return AirportCRUD


router = APIRouter(
    prefix="/airports",
    tags=["Airport REST API operations"],
    responses={
        status.HTTP_400_BAD_REQUEST: RespAirportEnum.InvalidData.value,
    }
)


@router.get(
    "/", 
    status_code=status.HTTP_200_OK,
    response_model=list[Airport],
    responses={
        status.HTTP_200_OK: RespAirportEnum.GetAll.value,
    }
)
async def get_all_airports(
        db: Annotated[Session, Depends(get_db)], 
        airportCRUD: Annotated[IAirportCRUD, Depends(get_airport_crud)],
        page: Annotated[int, Query(ge=1)] = 1,
        size: Annotated[int, Query(ge=1)] = 100
    ):
    return await AirportService(
            airportCRUD=airportCRUD,
            db=db
        ).get_all(
            page=page, 
            size=size
        )


@router.get(
    "/{airport_id}/", 
    status_code=status.HTTP_200_OK,
    response_model=Airport,
    responses={
        status.HTTP_200_OK: RespAirportEnum.GetByID.value,
        status.HTTP_404_NOT_FOUND: RespAirportEnum.NotFound.value,
    }
)
async def get_airport_by_id(
        db: Annotated[Session, Depends(get_db)], 
        airportCRUD: Annotated[IAirportCRUD, Depends(get_airport_crud)],
        airport_id: int
    ):
    return await AirportService(
            airportCRUD=airportCRUD,
            db=db,
        ).get_by_id(airport_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    responses={
        status.HTTP_201_CREATED: RespAirportEnum.Created.value,
    }
)
async def create_new_airport(
        db: Annotated[Session, Depends(get_db)],
        airportCRUD: Annotated[IAirportCRUD, Depends(get_airport_crud)],
        airport_create: AirportCreate
    ):
    airport = await AirportService(
            airportCRUD=airportCRUD,
            db=db,
        ).add(airport_create)
    
    return Response(
            status_code=status.HTTP_201_CREATED,
            headers={"Location": f"/api/v1/airports/{airport.id}"}
        )


@router.delete(
    "/{airport_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_204_NO_CONTENT: RespAirportEnum.Delete.value,
        status.HTTP_404_NOT_FOUND: RespAirportEnum.NotFound.value,
    }
)
async def remove_airport_by_id(
        db: Annotated[Session, Depends(get_db)],
        airportCRUD: Annotated[IAirportCRUD, Depends(get_airport_crud)], 
        airport_id: int
    ):
    airport = await AirportService(
            airportCRUD=airportCRUD,
            db=db,
        ).delete(airport_id)
    
    return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
