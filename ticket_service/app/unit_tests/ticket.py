from copy import deepcopy
from uuid import UUID

from cruds.mocks.ticket import TicketMockCRUD
from cruds.mocks.data import TicketDataMock
from services.ticket import TicketService
from schemas.ticket import TicketFilter, TicketCreate, TicketUpdate
from enums.sort import SortTicket
from enums.status import TicketStatus
from models.ticket import TicketModel
from exceptions.http_exceptions import NotFoundException, ConflictException


ticketService = TicketService(
    ticketCRUD=TicketMockCRUD,
    db=None
)
correct_tickets = deepcopy(TicketDataMock._tickets)


def model_into_dict(model: TicketModel) -> dict:
    dictionary = model.__dict__
    del dictionary["_sa_instance_state"]
    return dictionary


async def test_get_all_tickets_success():
    try:
        tickets = await ticketService.get_all(
            ticket_filter=TicketFilter(), 
            sort_field=SortTicket.IdAsc,
        )

        assert len(tickets) == len(correct_tickets)
        for i in range(len(tickets)):
            assert model_into_dict(tickets[i]) == correct_tickets[i]
    except:
        assert False


async def test_get_ticket_by_uid_success():
    try:
        ticket = await ticketService.get_by_uid("37fa1f9b-293a-4639-93ff-e67afd5cf5ea")

        assert model_into_dict(ticket) == correct_tickets[0]
    except:
        assert False


async def test_get_ticket_by_uid_not_found():
    try:
        await ticketService.get_by_uid("00ff0f0f-00f-0000-00ff-f00fff0ff0ff")

        assert False
    except NotFoundException:
        assert True
    except:
        assert False


async def test_add_ticket_success():
    try:
        ticket = await ticketService.add(
            TicketCreate(
                username="Test user",
                flight_number="QwErTy",
                price=1000,
                status=TicketStatus.Paid.value
            )
        )
        
        assert \
            ticket.username == "Test user" and \
            ticket.flight_number == "QwErTy" and \
            ticket.price == 1000 and \
            ticket.status == TicketStatus.Paid.value and \
            ticket.id == correct_tickets[-1]["id"] + 1 and \
            type(ticket.ticket_uid) == UUID
    except:
        assert False

async def test_delete_ticket_success():
    try:
        ticket = await ticketService.delete("37fa1f9b-293a-4639-93ff-e67afd5cf5ea")

        assert correct_tickets[0] == model_into_dict(ticket)
    except:
        assert False


async def test_delete_ticket_not_found():
    try:
        await ticketService.delete("00ff0f0f-00f-0000-00ff-f00fff0ff0ff")
        
        assert False
    except NotFoundException:
        assert True
    except:
        assert False


async def test_update_ticket_success():
    try:
        ticket = await ticketService.patch(
            ticket_uid="479fe41f-cd12-47ae-a366-d847c0ebbd01",
            ticket_update=TicketUpdate(
                status=TicketStatus.Canceled.value
            )
        )

        correct_ticket = deepcopy(correct_tickets[1])
        correct_ticket["status"] = TicketStatus.Canceled.value
        assert correct_ticket == model_into_dict(ticket)
    except:
        assert False


async def test_update_ticket_not_found():
    try:
        await ticketService.patch(
            ticket_uid="00ff0f0f-00f-0000-00ff-f00fff0ff0ff",
            ticket_update=TicketUpdate(
                status=TicketStatus.Canceled.value
            )
        )

        assert False
    except NotFoundException:
        assert True
    except:
        assert False
