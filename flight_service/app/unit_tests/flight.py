from copy import deepcopy
from datetime import datetime as dt

from cruds.mocks.flight import FlightMockCRUD
from cruds.mocks.data import FlightDataMock
from services.flight import FlightService
from schemas.flight import FlightFilter, FlightCreate
from models.flight import FlightModel
from exceptions.http_exceptions import NotFoundException, ConflictException


flightService = FlightService(
    flightCRUD=FlightMockCRUD,
    db=None
)
correct_flights = deepcopy(FlightDataMock._flights)


def model_into_dict(model: FlightModel) -> dict:
    dictionary = model.__dict__
    del dictionary["_sa_instance_state"]
    return dictionary


async def test_get_all_flights_success():
    try:
        flights = await flightService.get_all(
            flight_filter=FlightFilter()
        )

        assert len(flights) == len(correct_flights)
        for i in range(len(flights)):
            assert model_into_dict(flights[i]) == correct_flights[i]
    except:
        assert False


async def test_get_flight_by_id_success():
    try:
        flight = await flightService.get_by_id(1)

        assert model_into_dict(flight) == correct_flights[0]
    except:
        assert False


async def test_get_flight_by_id_not_found():
    try:
        await flightService.get_by_id(10)

        assert False
    except NotFoundException:
        assert True
    except:
        assert False


async def test_add_flight_success():
    try:
        flight = await flightService.add(
            FlightCreate(
                flight_number="AAA555",
                price=3000,
                datetime="2023-10-30T18:00:18.257Z",
                from_airport_id=2, 
                to_airport_id=1
            )
        )
        
        assert \
            flight.flight_number == "AAA555" and \
            flight.price == 3000 and \
            type(flight.datetime) == dt and \
            flight.from_airport_id == 2 and \
            flight.to_airport_id == 1 and \
            flight.id == correct_flights[-1]["id"] + 1 
    except:
        assert False

async def test_add_flight_conflict():
    try:
        await flightService.add(
            FlightCreate(
                flight_number="BCD987",
                price=3000,
                datetime="2023-10-30T18:00:18.257Z",
                from_airport_id=2, 
                to_airport_id=1
            )
        )
        
        assert False
    except ConflictException:
        assert True
    except:
        assert False

async def test_delete_flight_success():
    try:
        flight = await flightService.delete(3)

        assert correct_flights[2] == model_into_dict(flight)
    except:
        assert False


async def test_delete_flight_not_found():
    try:
        await flightService.delete(10)
        
        assert False
    except NotFoundException:
        assert True
    except:
        assert False
