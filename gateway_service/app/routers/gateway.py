from fastapi import APIRouter, Depends, status, Query, Header
from fastapi.responses import Response
from typing import Annotated
from uuid import UUID

from schemas.flight import PaginationResponse
from schemas.ticket import TicketResponse, TicketPurchaseResponse, TicketPurchaseRequest
from schemas.bonus import PrivilegeInfoResponse
from schemas.user import UserInfoResponse
from services.gateway import GatewayService
from enums.responses import RespEnum
from cruds.interfaces.flight import IFlightCRUD
from cruds.interfaces.ticket import ITicketCRUD
from cruds.interfaces.bonus import IBonusCRUD
from cruds.flight import FlightCRUD
from cruds.ticket import TicketCRUD
from cruds.bonus import BonusCRUD


def get_flight_crud() -> type[IFlightCRUD]:
    return FlightCRUD

def get_ticket_crud() -> type[ITicketCRUD]:
    return TicketCRUD

def get_bonus_crud() -> type[IBonusCRUD]:
    return BonusCRUD


router = APIRouter(
    tags=["Gateway API"],
    responses={
        status.HTTP_400_BAD_REQUEST: RespEnum.InvalidData.value,
    }
)


@router.get(
    "/flights", 
    status_code=status.HTTP_200_OK,
    response_model=PaginationResponse,
    responses={
        status.HTTP_200_OK: RespEnum.GetAllFlights.value,
    }
)
async def get_list_of_flights(
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        ticketCRUD: Annotated[ITicketCRUD, Depends(get_ticket_crud)],
        bonusCRUD:  Annotated[IBonusCRUD,  Depends(get_bonus_crud)],
        page: Annotated[int, Query(ge=1)] = 1,
        size: Annotated[int, Query(ge=1)] = 100
    ):
    return await GatewayService(
            flightCRUD=flightCRUD,
            ticketCRUD=ticketCRUD,
            bonusCRUD=bonusCRUD
        ).get_list_of_flights(
            page=page, 
            size=size
        )


@router.get(
    "/tickets", 
    status_code=status.HTTP_200_OK,
    response_model=list[TicketResponse],
    responses={
        status.HTTP_200_OK: RespEnum.GetAllTickets.value,
    }
)
async def get_information_on_all_user_tickets(
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        ticketCRUD: Annotated[ITicketCRUD, Depends(get_ticket_crud)],
        bonusCRUD:  Annotated[IBonusCRUD,  Depends(get_bonus_crud)],
        X_User_Name: Annotated[str, Header(max_length=80)]
    ):
    return await GatewayService(
            flightCRUD=flightCRUD,
            ticketCRUD=ticketCRUD,
            bonusCRUD=bonusCRUD
        ).get_info_on_all_user_tickets(
            user_name=X_User_Name
        )


@router.get(
    "/tickets/{ticketUid}", 
    status_code=status.HTTP_200_OK,
    response_model=TicketResponse,
    responses={
        status.HTTP_200_OK: RespEnum.GetTicket.value,
        status.HTTP_404_NOT_FOUND: RespEnum.TicketNotFound.value,
    }
)
async def get_information_on_user_ticket(
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        ticketCRUD: Annotated[ITicketCRUD, Depends(get_ticket_crud)],
        bonusCRUD:  Annotated[IBonusCRUD,  Depends(get_bonus_crud)],
        X_User_Name: Annotated[str, Header(max_length=80)],
        ticketUid: UUID
    ):
    return await GatewayService(
            flightCRUD=flightCRUD,
            ticketCRUD=ticketCRUD,
            bonusCRUD=bonusCRUD
        ).get_info_on_user_ticket(
            user_name=X_User_Name,
            ticket_uid=ticketUid
        )


@router.post(
    "/tickets", 
    status_code=status.HTTP_200_OK,
    response_model=TicketPurchaseResponse,
    responses={
        status.HTTP_200_OK: RespEnum.BuyTicket.value,
        status.HTTP_404_NOT_FOUND: RespEnum.FlightNumberNotFound.value,
    }
)
async def buy_ticket(
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        ticketCRUD: Annotated[ITicketCRUD, Depends(get_ticket_crud)],
        bonusCRUD:  Annotated[IBonusCRUD,  Depends(get_bonus_crud)],
        X_User_Name: Annotated[str, Header(max_length=80)],
        ticket_purchase_request: TicketPurchaseRequest
    ):
    return await GatewayService(
            flightCRUD=flightCRUD,
            ticketCRUD=ticketCRUD,
            bonusCRUD=bonusCRUD
        ).buy_ticket(
            user_name=X_User_Name,
            ticket_purchase_request=ticket_purchase_request
        )


@router.delete(
    "/tickets/{ticketUid}", 
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_204_NO_CONTENT: RespEnum.TicketRefund.value,
        status.HTTP_404_NOT_FOUND: RespEnum.TicketNotFound.value,
    }
)
async def ticket_refund(
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        ticketCRUD: Annotated[ITicketCRUD, Depends(get_ticket_crud)],
        bonusCRUD:  Annotated[IBonusCRUD,  Depends(get_bonus_crud)],
        X_User_Name: Annotated[str, Header(max_length=80)],
        ticketUid: UUID
    ):
    ticket_dict = await GatewayService(
            flightCRUD=flightCRUD,
            ticketCRUD=ticketCRUD,
            bonusCRUD=bonusCRUD
        ).ticket_refund(
            user_name=X_User_Name,
            ticket_uid=ticketUid
        )
    
    return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )


@router.get(
    "/me", 
    status_code=status.HTTP_200_OK,
    response_model=UserInfoResponse,
    responses={
        status.HTTP_200_OK: RespEnum.GetMe.value,
    }
)
async def get_user_information(
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        ticketCRUD: Annotated[ITicketCRUD, Depends(get_ticket_crud)],
        bonusCRUD:  Annotated[IBonusCRUD,  Depends(get_bonus_crud)],
        X_User_Name: Annotated[str, Header(max_length=80)],
    ):
    return await GatewayService(
            flightCRUD=flightCRUD,
            ticketCRUD=ticketCRUD,
            bonusCRUD=bonusCRUD
        ).get_user_information(
            user_name=X_User_Name,
        )


@router.get(
    "/privilege", 
    status_code=status.HTTP_200_OK,
    response_model=PrivilegeInfoResponse,
    responses={
        status.HTTP_200_OK: RespEnum.GetPrivilege.value,
    }
)
async def get_information_about_bonus_account(
        flightCRUD: Annotated[IFlightCRUD, Depends(get_flight_crud)],
        ticketCRUD: Annotated[ITicketCRUD, Depends(get_ticket_crud)],
        bonusCRUD:  Annotated[IBonusCRUD,  Depends(get_bonus_crud)],
        X_User_Name: Annotated[str, Header(max_length=80)],
    ):
    return await GatewayService(
            flightCRUD=flightCRUD,
            ticketCRUD=ticketCRUD,
            bonusCRUD=bonusCRUD
        ).get_info_about_bonus_account(
            user_name=X_User_Name,
        )
