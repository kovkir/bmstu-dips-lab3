from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

from models.flight import FlightModel
from schemas.flight import FlightFilter


class IFlightCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(
            self,
            flight_filter: FlightFilter,
            offset: int = 0,
            limit: int = 100
        ) -> list[FlightModel]:
       pass
    
    @abstractmethod
    async def get_by_id(self, flight_id: int) -> FlightModel | None:
        pass

    @abstractmethod
    async def add(self, ticket: FlightModel) -> FlightModel | None:
        pass
    
    @abstractmethod
    async def delete(self, ticket: FlightModel) -> FlightModel:
        pass
