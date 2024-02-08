from sqlalchemy.orm import Session

from models.privilege_history import PrivilegeHistoryModel
from schemas.privilege_history import PrivilegeHistoryCreate, PrivilegeHistoryFilter
from exceptions.http_exceptions import NotFoundException, ConflictException
from cruds.interfaces.privilege_history import IPrivilegeHistoryCRUD


class PrivilegeHistoryService():
    def __init__(
            self,
            privilegeHistoryCRUD: type[IPrivilegeHistoryCRUD], 
            db: Session
        ):
        self._privilegeHistoryCRUD = privilegeHistoryCRUD(db)
        
    async def get_all(
            self,
            privilege_history_filter: PrivilegeHistoryFilter
        ):
        return await self._privilegeHistoryCRUD.get_all(privilege_history_filter)

    async def get_by_id(self, privilege_history_id: int):
        privilege_history = await self._privilegeHistoryCRUD.get_by_id(privilege_history_id)
        if privilege_history == None:
            raise NotFoundException(prefix="Get Privilege History")
        
        return privilege_history
    
    async def add(self, privilege_history_create: PrivilegeHistoryCreate):
        privilege_history = PrivilegeHistoryModel(**privilege_history_create.model_dump())
        privilege_history = await self._privilegeHistoryCRUD.add(privilege_history)
        if privilege_history == None:
            raise ConflictException(
                    prefix="Add Privilege History",
                    message="не существует привилегии с таким id"
                )
        
        return privilege_history
    
    async def delete(self, privilege_history_id: int):
        privilege_history = await self._privilegeHistoryCRUD.get_by_id(privilege_history_id)
        if privilege_history == None:
            raise NotFoundException(prefix="Delete Privilege History")
