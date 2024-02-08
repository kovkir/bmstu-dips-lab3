from pydantic import BaseModel, constr, conint
from datetime import datetime as dt


def convert_datetime(datetime: dt) -> str:
    return datetime.strftime('%Y-%m-%d %H:%M')


class FlightResponse(BaseModel):
    flightNumber: constr(max_length=20)
    fromAirport: str | None
    toAirport: str | None
    date: dt
    price: conint(ge=1)

    class Config:
        json_encoders = {
            dt: convert_datetime
        }


class PaginationResponse(BaseModel):
    page: conint(ge=1)
    pageSize: conint(ge=1)
    totalElements: conint(ge=0)
    items: list[FlightResponse]
