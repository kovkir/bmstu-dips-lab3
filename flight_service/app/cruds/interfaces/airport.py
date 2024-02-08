from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

from models.airport import AirportModel


class IAirportCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100
        ) -> list[AirportModel]:
       pass
    
    @abstractmethod
    async def get_by_id(self, airport_id: int) -> AirportModel | None:
        pass

    @abstractmethod
    async def add(self, ticket: AirportModel) -> AirportModel | None:
        pass
    
    @abstractmethod
    async def delete(self, ticket: AirportModel) -> AirportModel:
        pass
