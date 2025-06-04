from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import List

class RepositoryBase(SQLModel):
    """Base model with common fields"""
    protocol: str = Field(primary_key=True)
    version: str = Field(primary_key=True)
    url: str

class Repository(RepositoryBase, table=True):
    """Database model for source repositories"""
    date_added: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

class RepositoryCreate(RepositoryBase):
    """Request model for creating source repository entries"""
    pass

class RepositoryUpdate(SQLModel):
    """Request model for updating source repository entries"""
    url: str

class RepositoryResponse(RepositoryBase):
    """Response model for source repository operations"""
    date_added: datetime
    last_updated: datetime

class RepositoryListResponse(SQLModel):
    """Response model for list of source repository entries"""
    total: int
    items: List[RepositoryResponse]