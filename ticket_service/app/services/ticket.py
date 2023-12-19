from sqlalchemy.orm import Session
from uuid import UUID

from models.ticket import TicketModel
from schemas.ticket import TicketFilter, TicketCreate, TicketUpdate
from exceptions.http_exceptions import NotFoundException, ConflictException
from cruds.interfaces.ticket import ITicketCRUD
from enums.sort import SortTicket


class TicketService():
    def __init__(self, ticketCRUD: type[ITicketCRUD], db: Session):
        self._ticketCRUD = ticketCRUD(db)
        
    async def get_all(
            self, 
            ticket_filter: TicketFilter,
            sort_field: SortTicket,
            page: int = 1, 
            size: int = 100
        ):
        return await self._ticketCRUD.get_all(
                ticket_filter=ticket_filter,
                sort_field=sort_field,
                offset=(page - 1) * size, 
                limit=size
            )

    async def get_by_uid(self, ticket_uid: UUID):
        ticket = await self._ticketCRUD.get_by_uid(ticket_uid)
        if ticket == None:
            raise NotFoundException(prefix="Get Ticket")
        
        return ticket
    
    async def add(self, ticket_create: TicketCreate):
        ticket = TicketModel(**ticket_create.model_dump())
        ticket = await self._ticketCRUD.add(ticket)
        if ticket == None:
            raise ConflictException(prefix="Add Ticket")
        
        return ticket
    
    async def delete(self, ticket_uid: UUID):
        ticket = await self._ticketCRUD.get_by_uid(ticket_uid)
        if ticket == None:
            raise NotFoundException(prefix="Delete Ticket")
        
        return await self._ticketCRUD.delete(ticket)
    
    async def patch(self, ticket_uid: UUID, ticket_update: TicketUpdate):
        ticket = await self._ticketCRUD.get_by_uid(ticket_uid)
        if ticket == None:
            raise NotFoundException(prefix="Update Ticket")
    
        ticket = await self._ticketCRUD.patch(ticket, ticket_update)
        if ticket == None:
            raise ConflictException(prefix="Update Ticket")
        
        return ticket
