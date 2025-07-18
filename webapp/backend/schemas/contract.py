from pydantic import BaseModel
from models.contract import ContractResponse
from models.audit import AuditResponse
from models.repository import RepositoryResponse
from typing import List

class ContractAuditCheckResponse(BaseModel):
    """Response model for contract audit check endpoint"""
    contract: ContractResponse
    audits: List[AuditResponse]

class ContractRepositoryResponse(BaseModel):
    """Response model for contract repository endpoint"""
    contract: ContractResponse
    repository: RepositoryResponse

class ContractAuditCreate(BaseModel):
    """Request model for adding audit to contract"""
    company: str
    url: str

class ContractRepositoryCreate(BaseModel):
    """Request model for adding repository to contract"""
    url: str
