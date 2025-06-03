from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class AuditBase(SQLModel):
    """Base model with common fields"""
    protocol: str = Field(primary_key=True)
    version: str = Field(primary_key=True)
    company: str = Field(primary_key=True)
    url: str

class Audit(AuditBase, table=True):
    """Database model for audit entries"""
    date_added: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

    class Config:
        table_name = "audit"

class AuditCreate(AuditBase):
    """Request model for creating audit entries"""
    pass

class AuditUpdate(SQLModel):
    """Schema for updating audit entries"""
    url: str

class AuditResponse(AuditBase):
    """Response schema for audit entries"""
    date_added: datetime
    last_updated: datetime

class AuditListResponse(SQLModel):
    """Response schema for list of audits"""
    total: int
    items: list[AuditResponse]
