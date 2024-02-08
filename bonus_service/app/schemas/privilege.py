from pydantic import BaseModel, constr, conint

from enums.status import PrivilegeStatus


class PrivilegeBase(BaseModel):
    username: constr(max_length=80)
    status: PrivilegeStatus
    balance: conint(ge=0) | None


class PrivilegeFilter(BaseModel):
    username: constr(max_length=80) | None = None
    status: PrivilegeStatus | None = None
    

class PrivilegeUpdate(BaseModel):
    status: PrivilegeStatus | None = None
    balance: conint(ge=0) | None = None


class PrivilegeCreate(PrivilegeBase):
    status: PrivilegeStatus = 'BRONZE'
    balance: conint(ge=0) | None = None


class Privilege(PrivilegeBase):
    id: int
