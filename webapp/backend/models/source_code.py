from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class SourceCodeBase(SQLModel):
    """Base model with common fields"""
    protocol: str = Field(primary_key=True)
    version: str = Field(primary_key=True)
    url: str

class SourceCode(SourceCodeBase, table=True):
    """Database model for source code repositories"""
    date_added: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

    class Config:
        table_name = "source-code"

class SourceCodeCreate(SourceCodeBase):
    """Request model for creating source code entries"""
    pass

class SourceCodeUpdate(SQLModel):
    """Request model for updating source code entries"""
    url: str

class SourceCodeResponse(SourceCodeBase):
    """Response model for source code operations"""
    date_added: datetime
    last_updated: datetime

class SourceCodeListResponse(SQLModel):
    """Response model for list of source code entries"""
    total: int
    items: list[SourceCodeResponse]