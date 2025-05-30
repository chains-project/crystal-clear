from sqlmodel import SQLModel, Field
from datetime import datetime

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
