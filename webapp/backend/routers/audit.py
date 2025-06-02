from fastapi import APIRouter, Depends, HTTPException, status
from models.audit import (
    Audit,
    AuditRequest,
    AuditResponse,
    AuditUpdate,
    AuditListResponse
)
from schemas.response import ErrorResponse

from core.database import get_session
from sqlalchemy.orm import Session
from services.audit_service import AuditService

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
)

def get_audit_service(session: Session = Depends(get_session)) -> AuditService:
    return AuditService(session)

@router.post(
    "/",
    response_model=AuditResponse,
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
    summary="Create a new audit entry",
)
async def create_audit(
    audit_data: AuditRequest,
    service: AuditService = Depends(get_audit_service),
):
    """
    Create a new audit entry.
    
    Args:
        audit_data: Data for the audit entry.
        session: SQLAlchemy session.
    
    Returns:
        Created audit entry.
    
    Raises:
        HTTPException: If the input data is invalid or creation fails.
    """
    print(f"Creating audit entry with data: {audit_data}")
    audit = await service.create_audit(audit_data)
    return audit

@router.get(
    "/{id}",
    response_model=AuditResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Audit not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Get audit entry by ID",
)
async def get_audit(
    id: int,
    service: AuditService = Depends(get_audit_service),
):
    """
    Get an audit entry by ID.
    
    Args:
        id: ID of the audit entry to retrieve.
        session: SQLAlchemy session.
    
    Returns:
        Audit entry if found, raises HTTPException if not found.
    """
    audit = await service.get_audit(id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Audit not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Delete audit entry by ID",
    description="Delete an audit entry by its ID.",
)
async def delete_audit(
    id: int,
    service: AuditService = Depends(get_audit_service),
):
    """
    Delete an audit entry by ID.
    
    Args:
        id: ID of the audit entry to delete.
        session: SQLAlchemy session.
    
    Returns:
        No content if deletion is successful, raises HTTPException if not found.
    """
    audit = await service.delete_audit(id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return {"detail": "Audit deleted successfully"}

@router.get(
    "/",
    response_model=AuditListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Get audit entries",
)
async def get_audits(
    protocol: str | None = None,
    version: str | None = None,
    company: str | None = None,
    service: AuditService = Depends(get_audit_service),
):
    audits = await service.get_audits(protocol, version, company)
    print(audits)
    return AuditListResponse(
        total=len(audits),
        items=audits
    )

@router.put(
    "/{id}",
    response_model=AuditResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid input data"
        },
        404: {
            "model": ErrorResponse,
            "description": "Audit not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Update audit entry by ID",
)
async def update_audit(
    id: int,
    audit_data: AuditUpdate,
    service: AuditService = Depends(get_audit_service),
):
    """
    Update an existing audit entry by ID.
    
    Args:
        id: ID of the audit entry to update.
        audit_data: Data for the updated audit entry.
        session: SQLAlchemy session.
    
    Returns:
        Updated audit entry if successful, raises HTTPException if not found.
    """
    print(f"Updating audit entry with ID {id} and data: {audit_data}")
    audit = await service.update_audit(id, audit_data)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit