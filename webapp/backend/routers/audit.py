from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_session
from models.audit import Audit, AuditCreate
import services.audit_service as service

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
)

@router.post(
    "/",
    response_model=Audit,
    status_code=201,
    summary="Create a new audit entry",
    description="Create a new audit entry with the provided protocol, version, and company.",
)
async def create_audit(
    audit_data: AuditCreate,
    session: Session = Depends(get_session),
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
    audit = service.create_audit(session, audit_data)
    return audit

@router.get(
    "/{id}",
    response_model=Audit,
    status_code=200,
    summary="Get audit entry by ID",
    description="Retrieve an audit entry by its ID.",
)
async def get_audit(
    id: int,
    session: Session = Depends(get_session),
):
    """
    Get an audit entry by ID.
    
    Args:
        id: ID of the audit entry to retrieve.
        session: SQLAlchemy session.
    
    Returns:
        Audit entry if found, raises HTTPException if not found.
    """
    audit = service.get_audit(session, id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit

@router.delete(
    "/{id}",
    status_code=204,
    summary="Delete audit entry by ID",
    description="Delete an audit entry by its ID.",
)
async def delete_audit(
    id: int,
    session: Session = Depends(get_session),
):
    """
    Delete an audit entry by ID.
    
    Args:
        id: ID of the audit entry to delete.
        session: SQLAlchemy session.
    
    Returns:
        No content if deletion is successful, raises HTTPException if not found.
    """
    audit = service.delete_audit(session, id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return {"detail": "Audit deleted successfully"}

@router.get(
    "/",
    response_model=List[Audit],
    status_code=200,
    summary="Get audit entries",
    description="Retrieve audit entries with optional filters for protocol, version, and company.",
)
async def get_audits(
    protocol: str | None = None,
    version: str | None = None,
    company: str | None = None,
    session: Session = Depends(get_session),
):
    return await service.get_audits(session, protocol, version, company)
