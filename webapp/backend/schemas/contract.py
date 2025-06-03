from pydantic import BaseModel
from models.contract import ContractResponse
from models.audit import AuditResponse
from models.source_code import SourceCodeResponse
from typing import List

class ContractAuditCheckResponse(BaseModel):
    """Response model for contract audit check endpoint"""
    contract: ContractResponse
    audits: List[AuditResponse]

class ContractSourceCodeResponse(BaseModel):
    """Response model for contract source code endpoint"""
    contract: ContractResponse
    source_code: SourceCodeResponse
