from uuid import UUID, uuid4

from models.ticket import TicketModel
from schemas.ticket import TicketFilter, TicketUpdate
from enums.sort import SortTicket
from cruds.interfaces.ticket import ITicketCRUD
from cruds.mocks.data import TicketDataMock


class TicketMockCRUD(ITicketCRUD, TicketDataMock):
    async def get_all(
            self, 
            ticket_filter: TicketFilter,
            sort_field: SortTicket,
            offset: int = 0, 
            limit: int = 100
        ):
        tickets = [
            TicketModel(**item) for item in self._tickets
        ]
        tickets = await self.__filter_tickets(tickets, ticket_filter)
        tickets = await self.__sort_tickets(tickets, sort_field)
    
        return tickets[offset:limit]
    
    async def get_by_uid(self, ticket_uid: UUID):
        for item in self._tickets:
            if item["ticket_uid"] == ticket_uid:
                return TicketModel(**item)
            
        return None
    
    async def add(self, ticket: TicketModel):            
        self._tickets.append(
            {

                "username": ticket.username,
                "flight_number": ticket.flight_number,
                "price": ticket.price,
                "status": ticket.status,
                "ticket_uid": uuid4(),
                "id": 1 if len(self._tickets) == 0 
                        else self._tickets[-1]["id"] + 1
            },
        )
        
        return TicketModel(**self._tickets[-1])

    async def delete(self, ticket: TicketModel):
        for i in range(len(self._tickets)):
            item = self._tickets[i]
            if item["id"] == ticket.id:
                deleted_ticket = self._tickets.pop(i)
                break

        return TicketModel(**deleted_ticket)
    
    async def patch(self, ticket: TicketModel, ticket_update: TicketUpdate):
        update_fields = ticket_update.model_dump(mode='json', exclude_unset=True) 
        for item in self._tickets:
            if item["id"] == ticket.id:
                for key in update_fields:
                    item[key] = update_fields[key]

                updated_ticket = TicketModel(**item)
                break

        return updated_ticket
    
    async def __filter_tickets(self, tickets, ticket_filter: TicketFilter):
        return tickets
    
    async def __sort_tickets(self, tickets, sort_field: SortTicket):    
        return tickets
