from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime as dt

from utils.database import Base
from models.privilege import PrivilegeModel


class PrivilegeHistoryModel(Base):
    __tablename__ = "privilege_history"
    __table_args__ = {'extend_existing': True}
    
    id             = Column(Integer, primary_key=True, index=True)
    privilege_id   = Column(Integer, ForeignKey(PrivilegeModel.id))
    ticket_uid     = Column(UUID(as_uuid=True), nullable=False)
    datetime       = Column(DateTime(), nullable=False, default=dt.utcnow)
    balance_diff   = Column(Integer,    nullable=False)
    operation_type = Column(String(20), nullable=False)
