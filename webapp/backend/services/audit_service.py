from sqlmodel import Session

from core.exceptions import InputValidationError, InternalServerError
from core.database import get_session
import crud.audit
from models.audit import AuditCreate, Audit

def create_audit(session: Session, audit_data: AuditCreate) -> AuditCreate:
    """
    Create a new audit entry.

    Args:
        session: SQLAlchemy session
        audit_data: Data for the audit entry

    Returns:
        Created audit entry

    Raises:
        InputValidationError: If the input data is invalid
        InternalServerError: If the creation fails
    """
    try:
        if not audit_data.protocol or not audit_data.company:
            raise InputValidationError("Protocol and company are required fields.")

        audit = crud.audit.create_audit(session, audit_data)
        return audit
    except Exception as e:
        raise InternalServerError(f"Failed to create audit: {str(e)}") from e

def delete_audit(session: Session, id: int) -> bool:
    """
    Delete an audit entry by ID.

    Args:
        session: SQLAlchemy session
        id: ID of the audit entry to delete

    Returns:
        True if deletion was successful, False otherwise

    Raises:
        InternalServerError: If the deletion fails
    """
    try:
        success = crud.audit.delete_audit(session, id)
        if not success:
            raise InternalServerError(f"Audit with ID {id} not found.")
        return True
    except Exception as e:
        raise InternalServerError(f"Failed to delete audit: {str(e)}") from e

def get_audit(session: Session, id: int) -> Audit | None:
    """
    Get an audit entry by ID.

    Args:
        session: SQLAlchemy session
        id: ID of the audit entry to retrieve

    Returns:
        Audit entry if found, None otherwise

    Raises:
        InternalServerError: If the retrieval fails
    """
    try:
        audit = crud.audit.get_audit(session, id)
        if not audit:
            raise InternalServerError(f"Audit with ID {id} not found.")
        return audit
    except Exception as e:
        raise InternalServerError(f"Failed to get audit: {str(e)}") from e

def get_audits(
    session: Session,
    protocol: str = None,
    version: str = None,
    company: str = None
) -> list[Audit]:
    """
    Get a list of audits based on optional filters.

    Args:
        session: SQLAlchemy session
        protocol: Filter by protocol (optional)
        version: Filter by version (optional)
        company: Filter by company (optional)

    Returns:
        List of audit entries matching the filters

    Raises:
        InternalServerError: If the retrieval fails
    """
    try:
        audits = crud.audit.get_audits(session, protocol, version, company)
        return audits
    except Exception as e:
        raise InternalServerError(f"Failed to get audits: {str(e)}") from e

