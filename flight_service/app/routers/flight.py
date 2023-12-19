from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime as dt

from schemas.flight import FlightFilter, FlightCreate, Flight
from services.flight import FlightService
from enums.responses import RespFlightEnum
from utils.database import get_db
from cruds.interfaces.flight import IFlightCRUD
from cruds.flight import FlightCRUD
# from cruds.mocks.flight import FlightMockCRUD


def get_flight_crud() -> type[IFlightCRUD]:
    return FlightCRUD


router = APIRouter(
    prefix="/flights",
    tags=["Flight REST API operations"],
    responses={
        status.HTTP_400_BAD_REQUEST: RespFlightEnum.InvalidData.value,
    }
)


@router.get(
    "/", 
    status_code=status.HTTP_200_OK,
    response_model=list[Flight],
    responses={
        status.HTTP_200_OK: RespFlightEnum.GetAll.value,
    }
)
async def get_all_flights(
        db: Annotated[Session, Depends(get_db)], 
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        flight_number: Annotated[str | None, Query(max_length=20)] = None,
        min_price: Annotated[int | None, Query(ge=1)] = None,
        max_price: Annotated[int | None, Query(ge=1)] = None,
        datetime: dt | None = None,
        from_airport_id: Annotated[int | None, Query(ge=1)] = None,
        to_airport_id:   Annotated[int | None, Query(ge=1)] = None,
        page: Annotated[int, Query(ge=1)] = 1,
        size: Annotated[int, Query(ge=1)] = 100
    ):
    return await FlightService(
            flightCRUD=flightCRUD,
            db=db
        ).get_all(
            flight_filter=FlightFilter(
                flight_number=flight_number,
                min_price=min_price,
                max_price=max_price,
                datetime=datetime,
                from_airport_id=from_airport_id,
                to_airport_id=to_airport_id
            ),
            page=page, 
            size=size
        )


@router.get(
    "/{flight_id}/", 
    status_code=status.HTTP_200_OK,
    response_model=Flight,
    responses={
        status.HTTP_200_OK: RespFlightEnum.GetByID.value,
        status.HTTP_404_NOT_FOUND: RespFlightEnum.NotFound.value,
    }
)
async def get_flight_by_id(
        db: Annotated[Session, Depends(get_db)], 
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        flight_id: int
    ):
    return await FlightService(
            flightCRUD=flightCRUD,
            db=db,
        ).get_by_id(flight_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    responses={
        status.HTTP_201_CREATED: RespFlightEnum.Created.value,
        status.HTTP_409_CONFLICT: RespFlightEnum.Conflict.value,
    }
)
async def create_new_flight(
        db: Annotated[Session, Depends(get_db)], 
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)], 
        flight_create: FlightCreate
    ):
    flight = await FlightService(
            flightCRUD=flightCRUD,
            db=db,
        ).add(flight_create)
    
    return Response(
            status_code=status.HTTP_201_CREATED,
            headers={"Location": f"/api/v1/flights/{flight.id}"}
        )


@router.delete(
    "/{flight_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_204_NO_CONTENT: RespFlightEnum.Delete.value,
        status.HTTP_404_NOT_FOUND: RespFlightEnum.NotFound.value,
    }
)
async def remove_flight_by_id(
        db: Annotated[Session, Depends(get_db)],
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)], 
        flight_id: int
    ):
    flight = await FlightService(
            flightCRUD=flightCRUD,
            db=db,
        ).delete(flight_id)
    
    return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
