from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from models.contract import Contract, ContractCreate
from services.contract_service import ContractService
from core.database import get_session

router = APIRouter(
    prefix="/contract",
    tags=["contract"],
)

def get_contract_service(session: Session = Depends(get_session)) -> ContractService:
    return ContractService(session)

@router.post(
    "/",
    response_model=Contract,
    status_code=201,
    summary="Create a new contract",
)
async def create_contract(
    contract_data: ContractCreate,
    service: ContractService = Depends(get_contract_service),
):
    return await service.create_contract(contract_data)

@router.get(
    "/{address}",
    response_model=Contract,
    summary="Get contract by address",
)
async def get_contract(
    address: str,
    service: ContractService = Depends(get_contract_service),
):
    return await service.get_contract(address)

@router.put(
    "/{address}",
    response_model=Contract,
    summary="Update contract by address",
)
async def update_contract(
    address: str,
    contract_data: ContractCreate,
    service: ContractService = Depends(get_contract_service),
):
    return await service.update_contract(address, contract_data)

@router.delete(
    "/{address}",
    status_code=204,
    summary="Delete contract by address",
)
async def delete_contract(
    address: str,
    service: ContractService = Depends(get_contract_service),
):
    await service.delete_contract(address)
    return {"detail": "Contract deleted successfully"}

@router.get(
    "/",
    response_model=List[Contract],
    summary="Get all contracts",
)
async def get_contracts(
    protocol: str | None = None,
    version: str | None = None,
    service: ContractService = Depends(get_contract_service),
):
    return await service.get_contracts(protocol, version)

@router.get(
    "/{address}/audit",
    response_model=Dict,
    summary="Check if contract has an audit",
    description="Check if a contract has an associated audit report based on protocol and version.",
)
async def check_contract_audit(
    address: str,
    service: ContractService = Depends(get_contract_service),
):
    """
    Check if a contract has an associated audit.
    
    Args:
        address: The contract address to check
        
    Returns:
        Dict containing:
        - contract: Contract details
        - has_audit: Boolean indicating if audit exists
        - audit: Audit details if found, null if not found
    """
    return await service.check_contract_audit(address)