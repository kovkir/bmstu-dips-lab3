from models.flight import FlightModel
from schemas.flight import FlightFilter
from cruds.interfaces.flight import IFlightCRUD
from cruds.mocks.data import FlightDataMock


class FlightMockCRUD(IFlightCRUD, FlightDataMock):
    async def get_all(
            self,
            flight_filter: FlightFilter,
            offset: int = 0,
            limit: int = 100
        ):
        flights = [
            FlightModel(**item) for item in self._flights
        ]
        flights = await self.__filter_flights(flights, flight_filter)
    
        return flights[offset:limit]
    
    async def get_by_id(self, flight_id: int):
        for item in self._flights:
            if item["id"] == flight_id:
                return FlightModel(**item)
            
        return None
    
    async def add(self, flight: FlightModel):   
        for item in self._flights:
            if item["flight_number"] == flight.flight_number:
                return None
                     
        self._flights.append(
            {
                "flight_number": flight.flight_number,
                "price": flight.price,
                "datetime": flight.datetime,
                "from_airport_id": flight.from_airport_id,
                "to_airport_id": flight.to_airport_id,
                "id": 1 if len(self._flights) == 0 
                        else self._flights[-1]["id"] + 1
            },
        )
        
        return FlightModel(**self._flights[-1])

    async def delete(self, flight: FlightModel):
        for i in range(len(self._flights)):
            item = self._flights[i]
            if item["id"] == flight.id:
                deleted_flight = self._flights.pop(i)
                break

        return FlightModel(**deleted_flight)
    
    async def __filter_flights(self, flights, flight_filter: FlightFilter):
        return flights
