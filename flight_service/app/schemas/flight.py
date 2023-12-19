from pydantic import BaseModel, constr, conint
from datetime import datetime as dt


def convert_datetime_to_iso_8601_without_time_zone(datetime: dt) -> str:
    return datetime.strftime('%Y-%m-%d %H:%M')


class FlightBase(BaseModel):
    flight_number: constr(max_length=20)
    price: conint(ge=1)
    datetime: dt
    from_airport_id: conint(ge=1) | None
    to_airport_id: conint(ge=1) | None


class FlightFilter(BaseModel):
    flight_number: constr(max_length=20) | None = None
    min_price: conint(ge=1) | None = None
    max_price: conint(ge=1) | None = None
    datetime: dt | None = None
    from_airport_id: conint(ge=1) | None = None
    to_airport_id: conint(ge=1) | None = None


class FlightCreate(FlightBase):
    from_airport_id: conint(ge=1) | None = None
    to_airport_id: conint(ge=1) | None = None


class Flight(FlightBase):
    id: int

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            dt: convert_datetime_to_iso_8601_without_time_zone
        }
