from sqlmodel import Session, select
from models.audit import Audit, AuditCreate, AuditUpdate
from typing import List
from datetime import datetime

def create_audit(session: Session, audit_data: AuditCreate) -> Audit:
    audit = Audit(**audit_data.model_dump())
    session.add(audit)
    session.commit()
    session.refresh(audit)
    return audit


def get_audit(session: Session, id: int) -> Audit | None:
    return session.get(Audit, id)

def delete_audit(session: Session, id: int) -> bool:
    audit = session.get(Audit, id)
    if not audit:
        return False
    session.delete(audit)
    session.commit()
    return True

def get_audits(session: Session, protocol: str = None, version: str = None, company: str = None) -> List[Audit]:
    stmt = select(Audit)
    
    if protocol:
        stmt = stmt.where(Audit.protocol == protocol)
    if version:
        stmt = stmt.where(Audit.version == version)
    if company:
        stmt = stmt.where(Audit.company == company)
    
    return session.exec(stmt).all()

def update_audit(session: Session, id: int, audit_data: AuditUpdate) -> Audit | None:
    """
    Update an audit entry with optional fields.
    Only updates fields that are provided in audit_data.
    
    Args:
        session: Database session
        id: ID of the audit to update
        audit_data: AuditUpdate model with optional fields
    
    Returns:
        Updated Audit object or None if not found
    """
    audit = session.get(Audit, id)
    if not audit:
        return None
        
    # Only update fields that are not None
    update_data = audit_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(audit, key, value)
    
    # Update last_updated timestamp
    audit.last_updated = datetime.now()
    
    session.commit()
    session.refresh(audit)
    return audit
