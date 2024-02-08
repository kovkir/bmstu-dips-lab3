from abc import ABC, abstractmethod

from schemas.bonus import (
    PrivilegeHistoryCreate, 
    PrivilegeHistoryFilter,
    PrivilegeCreate,
    PrivilegeUpdate
)


class IBonusCRUD(ABC):
    @abstractmethod
    async def get_all_privileges(
            self, 
            page: int = 0, 
            size: int = 100,
            username: str | None = None
        ) -> list[dict]:
        pass
    
    @abstractmethod
    async def get_privilege_by_id(self, privilege_id: int) -> dict:
        pass
    
    @abstractmethod
    async def create_new_privilege(self, privilege_create: PrivilegeCreate) -> int:
        pass
    
    @abstractmethod
    async def update_privilege_by_id(
            self, 
            privilege_id: int,
            privilege_update: PrivilegeUpdate
        ) -> dict:
        pass
    
    @abstractmethod
    async def get_all_privilege_histories(
            self, 
            ph_filter: PrivilegeHistoryFilter
        ) -> list[dict]:
        pass
    
    @abstractmethod
    async def create_new_privilege_history(
            self, 
            privilege_history_create: PrivilegeHistoryCreate
        ) -> int:
        pass
