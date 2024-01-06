import json
import requests
from requests import Response
from fastapi import status

from utils.settings import get_settings
from utils.curcuitBreaker import CircuitBreaker
from cruds.interfaces.bonus import IBonusCRUD
from cruds.base import BaseCRUD
from schemas.bonus import (
    PrivilegeHistoryCreate, 
    PrivilegeHistoryFilter,
    PrivilegeCreate, 
    PrivilegeUpdate,
)


class BonusCRUD(IBonusCRUD, BaseCRUD):
    def __init__(self):
        settings = get_settings()
        bonus_host = settings["services"]["gateway"]["bonus_host"]
        bonus_port = settings["services"]["bonus"]["port"]

        self.http_path = f'http://{bonus_host}:{bonus_port}/api/v1/'

    async def get_all_privileges(
            self,
            page: int = 1, 
            size: int = 100,
            username: str | None = None
        ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}privileges/?page={page}&size={size}'\
                f'{f"&username={username}" if username else ""}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Bonus Service"
        )
        
        return response.json()
    
    async def get_privilege_by_id(self, privilege_id: int):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}privileges/{privilege_id}/',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Bonus Service"
        )

        return response.json()
    
    async def create_new_privilege(self, privilege_create: PrivilegeCreate):
        try:
            response: Response = requests.post(
                url=f'{self.http_path}privileges/',
                data=json.dumps(privilege_create.model_dump())
            )
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        self._check_status_code(
            status_code=response.status_code,
            service_name="Bonus Service"
        )
        
        location: str = response.headers["location"]
        id_ = int(location.split("/")[-1])

        return id_
    
    async def update_privilege_by_id(
            self, 
            privilege_id: int,
            privilege_update: PrivilegeUpdate
        ):
        try:
            response: Response = requests.patch(
                url=f'{self.http_path}privileges/{privilege_id}/',
                data=json.dumps(privilege_update.model_dump(mode='json', exclude_unset=True))
            )
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        self._check_status_code(
            status_code=response.status_code,
            service_name="Bonus Service"
        )
        
        return response.json()
    
    async def get_all_privilege_histories(
            self, 
            ph_filter: PrivilegeHistoryFilter
        ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}privilege_histories/'\
                f'{f"?privilege_id={ph_filter.privilege_id}&" if ph_filter.privilege_id else "?"}'\
                f'{f"ticket_uid={ph_filter.ticket_uid}" if ph_filter.ticket_uid else ""}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Bonus Service"
        )
        
        return response.json()
    
    async def create_new_privilege_history(
            self,
            privilege_history_create: PrivilegeHistoryCreate
        ):
        try:
            response: Response = requests.post(
                url=f'{self.http_path}privilege_histories/',
                data=json.dumps(privilege_history_create.model_dump(mode='json', exclude_unset=True))
            )
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        self._check_status_code(
            status_code=response.status_code,
            service_name="Bonus Service"
        )
        
        location: str = response.headers["location"]
        id_ = int(location.split("/")[-1])

        return id_
    