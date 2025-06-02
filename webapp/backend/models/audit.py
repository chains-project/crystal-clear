from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Audit(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    protocol: str
    version: str
    company: str
    url: str
    date_added: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class AuditCreate(SQLModel):
    protocol: str
    version: str
    company: str
    url: str


class AuditResponse(SQLModel):
    """Response schema for audit entries"""
    id: int
    protocol: str
    version: str
    company: str
    url: str
    date_added: datetime
    last_updated: datetime


class AuditRequest(SQLModel):
    """Request schema for creating/updating audit entries"""
    protocol: str
    version: str
    company: str
    url: str


class AuditUpdate(SQLModel):
    """Schema for updating audit entries with optional fields"""
    protocol: Optional[str] = None
    version: Optional[str] = None
    company: Optional[str] = None
    url: Optional[str] = None


class AuditListResponse(SQLModel):
    """Response schema for list of audits"""
    total: int
    items: list[AuditResponse]
