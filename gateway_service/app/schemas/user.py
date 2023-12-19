from pydantic import BaseModel

from schemas.ticket import TicketResponse
from schemas.bonus import PrivilegeShortInfo


class UserInfoResponse(BaseModel):
    tickets: list[TicketResponse]
    privilege: PrivilegeShortInfo
