from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ContractBase(SQLModel):
    """Base model with common fields"""
    address: str
    protocol: str
    version: str

class Contract(ContractBase, table=True):
    """Database model for contracts"""
    id: int | None = Field(default=None, primary_key=True)
    address: str = Field(index=True)
    date_added: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

class ContractCreate(ContractBase):
    """Request model for creating contracts"""
    pass

class ContractUpdate(SQLModel):
    """Request model for updating contracts with optional fields"""
    protocol: Optional[str] = None
    version: Optional[str] = None

class ContractResponse(ContractBase):
    """Response model for contract operations"""
    id: int
    date_added: datetime
    last_updated: datetime

class ContractListResponse(SQLModel):
    """Response model for list of contracts"""
    total: int
    items: list[ContractResponse]
