import json
import requests
from requests import Response
from fastapi import status
from uuid import UUID

from utils.settings import get_settings
from utils.curcuitBreaker import CircuitBreaker
from schemas.ticket import TicketCreate, TicketUpdate
from cruds.interfaces.ticket import ITicketCRUD
from cruds.base import BaseCRUD


class TicketCRUD(ITicketCRUD, BaseCRUD):
    def __init__(self):
        settings = get_settings()
        ticket_host = settings["services"]["gateway"]["ticket_host"]
        ticket_port = settings["services"]["ticket"]["port"]

        self.http_path = f'http://{ticket_host}:{ticket_port}/api/v1/'

    async def get_all_tickets(
            self,
            page: int = 1,
            size: int = 100,
            username: str | None = None
        ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}tickets/?page={page}&size={size}'
                f'{f"&username={username}" if username else ""}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Ticket Service"
        )
        
        return response.json()
    
    async def get_ticket_by_uid(self, ticket_uid: UUID):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}tickets/{ticket_uid}/',
            http_method=requests.get
        )
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return None
        
        self._check_status_code(
            status_code=response.status_code,
            service_name="Ticket Service"
        )

        return response.json()
    
    async def create_new_ticket(self, ticket_create: TicketCreate):
        try:
            response: Response = requests.post(
                url=f'{self.http_path}tickets/',
                data=json.dumps(ticket_create.model_dump(mode='json', exclude_unset=True))
            )
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        self._check_status_code(
            status_code=response.status_code,
            service_name="Ticket Service"
        )
        
        location: str = response.headers["location"]
        uid = location.split("/")[-1]

        return uid
    
    async def update_ticket(self, ticket_uid: UUID, ticket_update: TicketUpdate):
        try:
            response: Response = requests.patch(
                url=f'{self.http_path}tickets/{ticket_uid}/',
                data=json.dumps(ticket_update.model_dump(mode='json', exclude_unset=True))
            )
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        self._check_status_code(
            status_code=response.status_code,
            service_name="Ticket Service"
        )
        
        return response.json()
    
    async def delete_ticket(self, ticket_uid: UUID):
        try:
            response: Response = requests.delete(
                url=f'{self.http_path}tickets/{ticket_uid}/'
            )
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        self._check_status_code(
            status_code=response.status_code,
            service_name="Ticket Service"
        )
