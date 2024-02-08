from uuid import UUID

from models.ticket import TicketModel
from schemas.ticket import TicketFilter, TicketUpdate
from cruds.interfaces.ticket import ITicketCRUD
from enums.sort import SortTicket


class TicketCRUD(ITicketCRUD):
    async def get_all(
            self, 
            ticket_filter: TicketFilter,
            sort_field: SortTicket,
            offset: int = 0, 
            limit: int = 100
        ):
        tickets = self._db.query(TicketModel)
        tickets = await self.__filter_tickets(tickets, ticket_filter)
        tickets = await self.__sort_tickets(tickets, sort_field)
    
        return tickets.offset(offset).limit(limit).all()
    
    async def get_by_uid(self, ticket_uid: UUID):
        return self._db.query(TicketModel).filter(
            TicketModel.ticket_uid == ticket_uid).first()
    
    async def add(self, ticket: TicketModel):
        try:
            self._db.add(ticket)
            self._db.commit()
            self._db.refresh(ticket)
        except:
            return None
        
        return ticket

    async def delete(self, ticket: TicketModel):
        self._db.delete(ticket)
        self._db.commit()
        
        return ticket
    
    async def patch(self, ticket: TicketModel, ticket_update: TicketUpdate):
        update_fields = ticket_update.model_dump(exclude_unset=True)        
        for key, value in update_fields.items():
            setattr(ticket, key, value)
        
        try:
            self._db.add(ticket)
            self._db.commit()
            self._db.refresh(ticket)
        except:
            return None
        
        return ticket
    
    async def __filter_tickets(self, tickets, ticket_filter: TicketFilter):
        if ticket_filter.username:
            tickets = tickets.filter(
                TicketModel.username == ticket_filter.username)
            
        if ticket_filter.flight_number:
            tickets = tickets.filter(
                TicketModel.flight_number == ticket_filter.flight_number)

        if ticket_filter.min_price:
            tickets = tickets.filter(
                TicketModel.price >= ticket_filter.min_price)

        if ticket_filter.max_price:
            tickets = tickets.filter(
                TicketModel.price <= ticket_filter.max_price)
        
        if ticket_filter.status:
            tickets = tickets.filter(
                TicketModel.status == ticket_filter.status.value)
        
        return tickets
    
    async def __sort_tickets(self, tickets, sort_field: SortTicket):
        match sort_field:
            case SortTicket.UsernameAsc:
                tickets = tickets.order_by(TicketModel.username)
            case SortTicket.UsernameDesc:
                tickets = tickets.order_by(TicketModel.username.desc())

            case SortTicket.FlightNumberAsc:
                tickets = tickets.order_by(TicketModel.flight_number)
            case SortTicket.FlightNumberDesc:
                tickets = tickets.order_by(TicketModel.flight_number.desc())

            case SortTicket.PriceAsc:
                tickets = tickets.order_by(TicketModel.price)
            case SortTicket.PriceDesc:
                tickets = tickets.order_by(TicketModel.price.desc())

            case SortTicket.StatusAsc:
                tickets = tickets.order_by(TicketModel.status)
            case SortTicket.StatusDesc:
                tickets = tickets.order_by(TicketModel.status.desc())

            case SortTicket.IdDesc:
                tickets = tickets.order_by(TicketModel.id.desc())
            case _:
                tickets = tickets.order_by(TicketModel.id)
        
        return tickets
