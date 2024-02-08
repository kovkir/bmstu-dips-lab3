from pydantic import BaseModel, constr, conint
from uuid import UUID

from enums.status import TicketStatus


class TicketBase(BaseModel):
    username: constr(max_length=80)
    flight_number: constr(max_length=20)
    price: conint(ge=0)
    status: TicketStatus


class TicketFilter(BaseModel):
    username: constr(max_length=80) | None = None
    flight_number: constr(max_length=20) | None = None
    min_price: conint(ge=0) | None = None
    max_price: conint(ge=0) | None = None
    status: TicketStatus | None = None


class TicketUpdate(BaseModel):
    status: TicketStatus


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    ticket_uid: UUID
