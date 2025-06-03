from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class SourceCodeBase(SQLModel):
    """Base model with common fields"""
    protocol: str = Field(index=True)
    version: str
    link: str

class SourceCode(SourceCodeBase, table=True):
    """Database model for source code repositories"""
    id: int | None = Field(default=None, primary_key=True)
    date_added: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

class SourceCodeCreate(SourceCodeBase):
    """Request model for creating source code entries"""
    pass

class SourceCodeUpdate(SQLModel):
    """Request model for updating source code entries"""
    protocol: Optional[str] = None
    version: Optional[str] = None
    link: Optional[str] = None

class SourceCodeResponse(SourceCodeBase):
    """Response model for source code operations"""
    id: int
    date_added: datetime
    last_updated: datetime

class SourceCodeListResponse(SQLModel):
    """Response model for list of source code entries"""
    total: int
    items: list[SourceCodeResponse]