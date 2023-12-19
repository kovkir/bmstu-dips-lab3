from abc import ABC, abstractmethod


class IFlightCRUD(ABC):
    @abstractmethod
    async def get_all_flights(
            self, 
            page: int = 1, 
            size: int = 100,
            flight_number: str | None = None
        ) -> list[dict]:
        pass
    
    @abstractmethod
    async def get_airport_by_id(self, airport_id: int) -> dict:
        pass
