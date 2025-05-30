from sqlmodel import SQLModel, Field
from datetime import datetime

class Contract(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    address: str = Field(index=True)
    protocol: str
    version: str
    date_added: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class ContractCreate(SQLModel):
    address: str
    protocol: str
    version: str
