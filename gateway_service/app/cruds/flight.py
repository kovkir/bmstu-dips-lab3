import requests
from requests import Response

from utils.settings import get_settings
from utils.curcuitBreaker import CircuitBreaker
from cruds.interfaces.flight import IFlightCRUD
from cruds.base import BaseCRUD


class FlightCRUD(IFlightCRUD, BaseCRUD):
    def __init__(self):
        settings = get_settings()
        flight_host = settings["services"]["gateway"]["flight_host"]
        flight_port = settings["services"]["flight"]["port"]

        self.http_path = f'http://{flight_host}:{flight_port}/api/v1/'

    async def get_all_flights(
            self,  
            page: int = 1, 
            size: int = 100,
            flight_number: str | None = None
        ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}flights/?page={page}&size={size}'\
                f'{f"&flight_number={flight_number}" if flight_number else ""}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Flight Service"
        )
        
        return response.json()
    
    async def get_airport_by_id(self, airport_id: int):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}airports/{airport_id}/',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Flight Service"
        )
        
        return response.json()
