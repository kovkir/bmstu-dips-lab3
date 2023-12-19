from abc import ABC, abstractmethod

from schemas.ticket import TicketCreate, TicketUpdate


class ITicketCRUD(ABC):
    @abstractmethod
    async def get_all_tickets(
            self, 
            page: int = 0,
            size: int = 100,
            username: str | None = None
        ) -> list[dict]:
        pass

    @abstractmethod
    async def get_ticket_by_uid(self, ticket_uid: str) -> dict:
        pass
    
    @abstractmethod
    async def create_new_ticket(self, ticket_create: TicketCreate) -> str:
        pass

    @abstractmethod
    async def update_ticket(
            self, 
            ticket_uid: str, 
            ticket_update: TicketUpdate
        ) -> dict:
        pass
    