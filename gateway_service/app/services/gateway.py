from uuid import UUID

from cruds.interfaces.flight import IFlightCRUD
from cruds.interfaces.ticket import ITicketCRUD
from cruds.interfaces.bonus import IBonusCRUD
from exceptions.http_exceptions import NotFoundException
from enums.status import TicketStatus, PrivilegeHistoryStatus, PrivilegeStatus
from schemas.user import UserInfoResponse
from schemas.flight import (
    PaginationResponse, 
    FlightResponse
)
from schemas.bonus import (
    PrivilegeShortInfo,
    PrivilegeInfoResponse,
    BalanceHistory,
    PrivilegeCreate,
    PrivilegeUpdate,
    PrivilegeHistoryCreate,
    PrivilegeHistoryFilter
)
from schemas.ticket import (
    TicketResponse,
    TicketCreate, 
    TicketUpdate,
    TicketPurchaseRequest, 
    TicketPurchaseResponse
)


class GatewayService():
    def __init__(
            self, 
            flightCRUD: type[IFlightCRUD],
            ticketCRUD: type[ITicketCRUD],
            bonusCRUD:  type[IBonusCRUD]
        ):
        self._flightCRUD = flightCRUD()
        self._ticketCRUD = ticketCRUD()
        self._bonusCRUD  = bonusCRUD()
        
    async def get_list_of_flights(self, page: int, size: int):
        flight_list = await self._flightCRUD.get_all_flights(
            page=page,
            size=size
        )

        flights = []
        for flight_dict in flight_list:
            from_airport = await self.__get_airport_by_id(flight_dict["from_airport_id"])
            to_airport = await self.__get_airport_by_id(flight_dict["to_airport_id"])

            flights.append(
                FlightResponse(
                    flightNumber=flight_dict["flight_number"],
                    fromAirport=from_airport,
                    toAirport=to_airport,
                    date=flight_dict["datetime"],
                    price=flight_dict["price"]
                )
            )

        return PaginationResponse(
                page=page,
                pageSize=size,
                totalElements=len(flights),
                items=flights
            )

    async def get_info_on_all_user_tickets(self, user_name: str):
        ticket_list = await self._ticketCRUD.get_all_tickets(
            username=user_name
        )

        tickets = []
        for ticket_dict in ticket_list:
            flight_dict  = await self.__get_flight_by_number(ticket_dict["flight_number"])
            from_airport = await self.__get_airport_by_id(flight_dict["from_airport_id"])
            to_airport   = await self.__get_airport_by_id(flight_dict["to_airport_id"])

            tickets.append(
                TicketResponse(
                    ticketUid=ticket_dict["ticket_uid"],
                    flightNumber=ticket_dict["flight_number"],
                    fromAirport=from_airport,
                    toAirport=to_airport,
                    date=flight_dict["datetime"],
                    price=ticket_dict["price"],
                    status=ticket_dict["status"],
                )
            )

        return tickets
    
    async def get_info_on_user_ticket(self, user_name: str, ticket_uid: UUID):
        ticket_dict = await self._ticketCRUD.get_ticket_by_uid(ticket_uid)
        if not ticket_dict or ticket_dict["username"] != user_name:
            raise NotFoundException(
                prefix="Get Ticket",
                message="Билета с таким UID у данного пользователя не существует"
            )
        
        flight_dict  = await self.__get_flight_by_number(ticket_dict["flight_number"])
        from_airport = await self.__get_airport_by_id(flight_dict["from_airport_id"])
        to_airport   = await self.__get_airport_by_id(flight_dict["to_airport_id"])

        return TicketResponse(
                ticketUid=ticket_dict["ticket_uid"],
                flightNumber=ticket_dict["flight_number"],
                fromAirport=from_airport,
                toAirport=to_airport,
                date=flight_dict["datetime"],
                price=ticket_dict["price"],
                status=ticket_dict["status"],
            )
    
    async def buy_ticket(
            self,
            user_name: str,
            ticket_purchase_request: TicketPurchaseRequest
        ):
        flight_dict = await self.__get_flight_by_number(
            ticket_purchase_request.flightNumber
        )
        if flight_dict == None:
            raise NotFoundException(
                prefix="Buy Ticket",
                message="Рейса с таким номером не существует"
            )
        
        privilege_dict = await self.__get_privilege_by_username(user_name)

        paid_by_bonuses, paid_by_money = await self.__paid_ticket(
            price=ticket_purchase_request.price,
            balance=privilege_dict["balance"],
            paid_from_balance=ticket_purchase_request.paidFromBalance
        )

        ticket_dict = await self.__get_new_ticket(
            username=user_name,
            flight_number=ticket_purchase_request.flightNumber,
            price=paid_by_money
        )

        if ticket_purchase_request.paidFromBalance:
            updated_privilege = await self.__write_off_bonuses(
                privilege_dict=privilege_dict,
                ticket_uid=ticket_dict["ticket_uid"],
                balance_diff=paid_by_bonuses
            )
        else:
            coeff = self.__get_bonus_accrual_coeff(privilege_dict["status"])

            updated_privilege = await self.__add_bonuses(
                privilege_dict=privilege_dict,
                ticket_uid=ticket_dict["ticket_uid"],
                balance_diff=round(paid_by_money * coeff)
            )

        from_airport = await self.__get_airport_by_id(flight_dict["from_airport_id"])
        to_airport = await self.__get_airport_by_id(flight_dict["to_airport_id"])

        return TicketPurchaseResponse(
                ticketUid=ticket_dict["ticket_uid"],
                flightNumber=flight_dict["flight_number"],
                fromAirport=from_airport,
                toAirport=to_airport,
                date=flight_dict["datetime"],
                price=ticket_purchase_request.price,
                paidByMoney=paid_by_money,
                paidByBonuses=paid_by_bonuses,
                status=ticket_dict["status"],
                privilege=PrivilegeShortInfo(**updated_privilege)
            )
    
    async def ticket_refund(self, user_name: str, ticket_uid: UUID):
        ticket_dict = await self._ticketCRUD.get_ticket_by_uid(ticket_uid)
        if not ticket_dict or ticket_dict["username"] != user_name:
            raise NotFoundException(
                prefix="Get Ticket",
                message="Билета с таким UID у данного пользователя не существует"
            )
        
        updated_ticket_dict = await self._ticketCRUD.update_ticket(
            ticket_uid=ticket_uid,
            ticket_update=TicketUpdate(
                status=TicketStatus.Canceled.value
            )
        )

        privilege_histories = await self._bonusCRUD.get_all_privilege_histories(
            PrivilegeHistoryFilter(
                ticket_uid=ticket_uid
            )
        )
        last_history_dict = privilege_histories[-1]
        privilege_dict = await self._bonusCRUD.get_privilege_by_id(
            privilege_id=last_history_dict["privilege_id"]
        )

        if last_history_dict["operation_type"] == PrivilegeHistoryStatus.FILL_IN_BALANCE:
            await self.__write_off_bonuses(
                privilege_dict=privilege_dict,
                ticket_uid=ticket_uid,
                balance_diff=last_history_dict["balance_diff"]
            )
        else:
            await self.__add_bonuses(
                privilege_dict=privilege_dict,
                ticket_uid=ticket_uid,
                balance_diff=last_history_dict["balance_diff"]
            )

        return updated_ticket_dict
    
    async def get_user_information(self, user_name: str):
        tickets = await self.get_info_on_all_user_tickets(user_name)
        privilege_dict = await self.__get_privilege_by_username(user_name)

        return UserInfoResponse(
                tickets=tickets,
                privilege=privilege_dict
            )
    
    async def get_info_about_bonus_account(self, user_name: str):
        privilege_dict = await self.__get_privilege_by_username(user_name)
        privilege_histories = await self._bonusCRUD.get_all_privilege_histories(
            PrivilegeHistoryFilter(
                privilege_id=privilege_dict["id"]
            )
        )

        histories = []
        for history in privilege_histories:
            histories.append(
                BalanceHistory(
                    date=history["datetime"],
                    ticketUid=history["ticket_uid"],
                    balanceDiff=history["balance_diff"],
                    operationType=history["operation_type"]
                )
            )

        return PrivilegeInfoResponse(
                balance=privilege_dict["balance"],
                status=privilege_dict["status"],
                history=histories
            )
    
    async def __write_off_bonuses(
            self,
            privilege_dict: dict,
            ticket_uid: UUID,
            balance_diff: int
        ):
        if balance_diff > privilege_dict["balance"]:
            balance_diff = privilege_dict["balance"]

        updated_privilege = await self._bonusCRUD.update_privilege_by_id(
            privilege_id=privilege_dict["id"],
            privilege_update=PrivilegeUpdate(
                balance=privilege_dict["balance"] - balance_diff
            )
        )

        await self._bonusCRUD.create_new_privilege_history(
            PrivilegeHistoryCreate(
                privilege_id=privilege_dict["id"],
                ticket_uid=ticket_uid,
                balance_diff=balance_diff,
                operation_type=PrivilegeHistoryStatus.DEBIT_THE_ACCOUNT.value
            )
        )

        return updated_privilege

    async def __add_bonuses(self,
            privilege_dict: dict,
            ticket_uid: UUID,
            balance_diff: int
        ):
        updated_privilege = await self._bonusCRUD.update_privilege_by_id(
            privilege_id=privilege_dict["id"],
            privilege_update=PrivilegeUpdate(
                balance=privilege_dict["balance"] + balance_diff
            )
        )

        await self._bonusCRUD.create_new_privilege_history(
            PrivilegeHistoryCreate(
                privilege_id=privilege_dict["id"],
                ticket_uid=ticket_uid,
                balance_diff=balance_diff,
                operation_type=PrivilegeHistoryStatus.FILL_IN_BALANCE.value
            )
        )

        return updated_privilege
    
    def __get_bonus_accrual_coeff(self, privilege_status: str) -> float:
        if privilege_status == PrivilegeStatus.GOLD.value:
            coeff = 0.1
        elif privilege_status == PrivilegeStatus.SILVER.value:
            coeff = 0.1
        else:
            coeff = 0.1

        return coeff

    async def __paid_ticket(
            self, 
            price: int, 
            balance: int, 
            paid_from_balance: bool
        ):
        paid_by_bonuses = min(price, balance) if paid_from_balance else 0
        paid_by_money = price - paid_by_bonuses

        return paid_by_bonuses, paid_by_money
        
    async def __get_airport_by_id(self, airport_id: int):
        if airport_id:
            airport_dict = await self._flightCRUD.get_airport_by_id(airport_id)
            airport = f"{airport_dict['city']} {airport_dict['name']}"
        else:
            airport = None

        return airport
    
    async def __get_flight_by_number(self, flight_number: str):
        flight_list = await self._flightCRUD.get_all_flights(
            flight_number=flight_number
        )
        flight_dict = flight_list[0] if len(flight_list) else None

        return flight_dict
    
    async def __get_privilege_by_username(self, username: str):
        privilege_list = await self._bonusCRUD.get_all_privileges(
            username=username
        )
        if len(privilege_list):
            privilege_dict = privilege_list[0]
        else:
            privilege_dict = await self.__get_new_privilege(username)

        return privilege_dict
    
    async def __get_new_privilege(self, username: str):
        privilege_id = await self._bonusCRUD.create_new_privilege(
            PrivilegeCreate(
                username=username,
                balance=0
            )
        )
        privilege_dict = await self._bonusCRUD.get_privilege_by_id(privilege_id)

        return privilege_dict
    
    async def __get_new_ticket(self, username: str, flight_number: str, price: str):
        ticket_uid = await self._ticketCRUD.create_new_ticket(
            TicketCreate(
                username=username,
                flight_number=flight_number,
                price=price,
                status=TicketStatus.Paid.value
            )
        )
        ticket_dict = await self._ticketCRUD.get_ticket_by_uid(ticket_uid)

        return ticket_dict
