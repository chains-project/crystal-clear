from pydantic import BaseModel
from models.contract import ContractResponse
from models.audit import AuditResponse
from typing import List

class ContractAuditCheckResponse(BaseModel):
    """Response model for contract audit check endpoint"""
    contract: ContractResponse
    audits: List[AuditResponse]