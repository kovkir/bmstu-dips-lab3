from models.airport import AirportModel
from cruds.interfaces.airport import IAirportCRUD


class AirportCRUD(IAirportCRUD):
    async def get_all(
            self,
            offset: int = 0, 
            limit: int = 100
        ):
        airports = self._db.query(AirportModel)
        
        return airports.offset(offset).limit(limit).all()
    
    async def get_by_id(self, airport_id: int):
        return self._db.query(AirportModel).filter(
            AirportModel.id == airport_id).first()
    
    async def add(self, airport: AirportModel):
        try:
            self._db.add(airport)
            self._db.commit()
            self._db.refresh(airport)
        except:
            return None
        
        return airport

    async def delete(self, airport: AirportModel):
        self._db.delete(airport)
        self._db.commit()
        
        return airport
