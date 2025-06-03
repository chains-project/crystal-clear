from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from core.database import get_session
from models.audit import (
    AuditCreate,
    AuditResponse,
    AuditUpdate,
    AuditListResponse
)
from schemas.response import ErrorResponse
import crud.audit

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
)

@router.post(
    "/",
    response_model=AuditResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Create a new audit entry",
)
async def create_audit(
    audit_data: AuditCreate,
    session: Session = Depends(get_session),
) -> AuditResponse:
    """Create new audit entry"""
    try:
        return crud.audit.create_audit(session, audit_data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create audit: {str(e)}"
        )

@router.get(
    "/{protocol}/{version}/{company}",
    response_model=AuditResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Audit not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get audit by protocol, version and company",
)
async def get_audit(
    protocol: str,
    version: str,
    company: str,
    session: Session = Depends(get_session),
) -> AuditResponse:
    """Get specific audit entry"""
    audit = crud.audit.get_audit(session, protocol, version, company)
    if not audit:
        raise HTTPException(
            status_code=404,
            detail="Audit not found"
        )
    return audit

@router.get(
    "/",
    response_model=AuditListResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="List audit entries",
)
async def list_audits(
    protocol: str | None = None,
    version: str | None = None,
    company: str | None = None,
    session: Session = Depends(get_session),
) -> AuditListResponse:
    """List audit entries with optional filters"""
    audits = crud.audit.get_audits(
        session,
        protocol=protocol,
        version=version,
        company=company
    )
    return AuditListResponse(total=len(audits), items=audits)

@router.put(
    "/{protocol}/{version}/{company}",
    response_model=AuditResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Audit not found"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Update audit url",
)
async def update_audit(
    protocol: str,
    version: str,
    company: str,
    audit_data: AuditUpdate,
    session: Session = Depends(get_session),
) -> AuditResponse:
    """Update audit entry"""
    audit = crud.audit.update_audit(session, protocol, version, company, audit_data)
    if not audit:
        raise HTTPException(
            status_code=404,
            detail="Audit not found"
        )
    return audit

@router.delete(
    "/{protocol}/{version}/{company}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Audit not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Delete audit entry",
)
async def delete_audit(
    protocol: str,
    version: str,
    company: str,
    session: Session = Depends(get_session),
) -> None:
    """Delete audit entry"""
    if not crud.audit.delete_audit(session, protocol, version, company):
        raise HTTPException(
            status_code=404,
            detail="Audit not found"
        )