from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.contract import (
    ContractCreate,
    ContractUpdate,
    ContractResponse,
    ContractListResponse
)
from services.contract_service import ContractService
from core.database import get_session
from schemas.contract import ContractAuditCheckResponse, ContractSourceCodeResponse
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
            "description": "Contract already exists"
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
) -> ContractResponse:
    return await service.create_contract(contract_data)

@router.get(
    "/{address}",
    response_model=ContractResponse,
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
) -> ContractResponse:
    return await service.get_contract(address)

@router.put(
    "/{address}",
    response_model=ContractResponse,
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
) -> ContractResponse:
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
) -> None:
    await service.delete_contract(address)

@router.get(
    "/",
    response_model=ContractListResponse,
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="List contracts with optional filters",
)
async def get_contracts(
    protocol: str | None = None,
    version: str | None = None,
    service: ContractService = Depends(get_contract_service),
) -> ContractListResponse:
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
async def get_contract_audits(
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
        - audits: List of audit details if found
    """
    result = await service.get_contract_audits(address)
    return ContractAuditCheckResponse(**result)

@router.get(
    "/{address}/source_code",
    response_model=ContractSourceCodeResponse,
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
    summary="Get contract source code",
    description="Fetch the source code for a contract by its address.",
)
async def get_contract_source_code(
    address: str,
    service: ContractService = Depends(get_contract_service),
):
    """
    Get the source code for a contract by its address.
    
    Args:
        address: The contract address to fetch source code for
        
    Returns:
        Response containing:
        - contract: Contract details
        - source_code: Source code content
    """
    result = await service.get_contract_source_code(address)
    return result