from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models.contract import (
    ContractCreate,
    ContractUpdate,
    ContractResponse,
    ContractListResponse
)
from services.contract_service import ContractService
from core.database import get_session
from schemas.contract import ContractAuditCheckResponse
from schemas.response import ErrorResponse

router = APIRouter(
    prefix="/contract",
    tags=["contract"],
)

def get_contract_service(session: Session = Depends(get_session)) -> ContractService:
    return ContractService(session)

@router.post(
    "/",
    response_model=ContractResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid input data"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Create a new contract",
)
async def create_contract(
    contract_data: ContractCreate,
    service: ContractService = Depends(get_contract_service),
):
    return await service.create_contract(contract_data)

@router.get(
    "/{address}",
    response_model=ContractResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Contract not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Get contract by address",
)
async def get_contract(
    address: str,
    service: ContractService = Depends(get_contract_service),
):
    return await service.get_contract(address)

@router.put(
    "/{address}",
    response_model=ContractResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Contract not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Update contract by address",
)
async def update_contract(
    address: str,
    contract_data: ContractUpdate,
    service: ContractService = Depends(get_contract_service),
):
    return await service.update_contract(address, contract_data)

@router.delete(
    "/{address}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Contract not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
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
    response_model=ContractListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Get all contracts",
)
async def get_contracts(
    protocol: str | None = None,
    version: str | None = None,
    service: ContractService = Depends(get_contract_service),
):
    contracts = await service.get_contracts(protocol, version)
    return ContractListResponse(
        total=len(contracts),
        items=contracts
    )

@router.get(
    "/{address}/audits",
    response_model=ContractAuditCheckResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Contract not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Check if contract has audits",
    description="Check if a contract has associated audit reports based on protocol and version.",
)
async def check_contract_audits(
    address: str,
    service: ContractService = Depends(get_contract_service),
):
    """
    Check if a contract has associated audits.
    
    Args:
        address: The contract address to check
        
    Returns:
        Response containing:
        - contract: Contract details
        - has_audits: Boolean indicating if audits exist
        - audits: List of audit details if found
    """
    result = await service.check_contract_audits(address)
    return ContractAuditCheckResponse(**result)