from models.flight import FlightModel
from cruds.interfaces.flight import IFlightCRUD
from schemas.flight import FlightFilter


class FlightCRUD(IFlightCRUD):
    async def get_all(
            self,
            flight_filter: FlightFilter,
            offset: int = 0,
            limit: int = 100
        ):
        flights = self._db.query(FlightModel)
        flights = await self.__filter_flights(flights, flight_filter)
        
        return flights.offset(offset).limit(limit).all()
    
    async def get_by_id(self, flight_id: int):
        return self._db.query(FlightModel).filter(
            FlightModel.id == flight_id).first()
    
    async def add(self, flight: FlightModel):
        try:
            self._db.add(flight)
            self._db.commit()
            self._db.refresh(flight)
        except:
            return None
        
        return flight

    async def delete(self, flight: FlightModel):
        self._db.delete(flight)
        self._db.commit()
        
        return flight

    async def __filter_flights(self, flights, flight_filter: FlightFilter):
        if flight_filter.flight_number:
            flights = flights.filter(
                FlightModel.flight_number == flight_filter.flight_number)
            
        if flight_filter.min_price:
            flights = flights.filter(
                FlightModel.price >= flight_filter.min_price)

        if flight_filter.max_price:
            flights = flights.filter(
                FlightModel.price <= flight_filter.max_price)
        
        if flight_filter.datetime:
            flights = flights.filter(
                FlightModel.datetime == flight_filter.datetime)
        
        if flight_filter.from_airport_id:
            flights = flights.filter(
                FlightModel.from_airport_id == flight_filter.from_airport_id)
        
        if flight_filter.to_airport_id:
            flights = flights.filter(
                FlightModel.to_airport_id == flight_filter.to_airport_id)
        
        return flights
