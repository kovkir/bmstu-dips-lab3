from sqlalchemy.orm import Session

from models.privilege import PrivilegeModel
from schemas.privilege import PrivilegeCreate, PrivilegeUpdate, PrivilegeFilter
from exceptions.http_exceptions import NotFoundException, ConflictException
from cruds.interfaces.privilege import IPrivilegeCRUD


class PrivilegeService():
    def __init__(self, privilegeCRUD: type[IPrivilegeCRUD], db: Session):
        self._privilegeCRUD = privilegeCRUD(db)
        
    async def get_all(
            self,
            privilege_filter: PrivilegeFilter,
            page: int = 1,
            size: int = 100
        ):
        return await self._privilegeCRUD.get_all(
                privilege_filter=privilege_filter,
                offset=(page - 1) * size, 
                limit=size
            )

    async def get_by_id(self, privilege_id: int):
        privilege = await self._privilegeCRUD.get_by_id(privilege_id)
        if privilege == None:
            raise NotFoundException(prefix="Get Privilege")
        
        return privilege
    
    async def add(self, privilege_create: PrivilegeCreate):
        privilege = PrivilegeModel(**privilege_create.model_dump())
        privilege = await self._privilegeCRUD.add(privilege)
        if privilege == None:
            raise ConflictException(prefix="Add Privilege")
        
        return privilege
    
    async def delete(self, privilege_id: int):
        privilege = await self._privilegeCRUD.get_by_id(privilege_id)
        if privilege == None:
            raise NotFoundException(prefix="Delete Privilege")
        
        return await self._privilegeCRUD.delete(privilege)

    async def patch(self, privilege_id: int, privilege_update: PrivilegeUpdate):
        privilege = await self._privilegeCRUD.get_by_id(privilege_id)
        if privilege == None:
            raise NotFoundException(prefix="Update Privilege")
    
        privilege = await self._privilegeCRUD.patch(privilege, privilege_update)
        if privilege == None:
            raise ConflictException(prefix="Update Privilege")
        
        return privilege
