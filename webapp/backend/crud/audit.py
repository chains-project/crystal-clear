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

def get_audit(
    session: Session, 
    protocol: str,
    version: str,
    company: str
) -> Audit | None:
    return session.get(Audit, {"protocol": protocol, "version": version, "company": company})

def delete_audit(
    session: Session,
    protocol: str,
    version: str,
    company: str
) -> bool:
    audit = get_audit(session, protocol, version, company)
    if not audit:
        return False
    session.delete(audit)
    session.commit()
    return True

def get_audits(
    session: Session, 
    protocol: str | None = None, 
    version: str | None = None, 
    company: str | None = None
) -> List[Audit]:
    stmt = select(Audit)
    
    if protocol:
        stmt = stmt.where(Audit.protocol == protocol)
    if version:
        stmt = stmt.where(Audit.version == version)
    if company:
        stmt = stmt.where(Audit.company == company)
    
    return session.exec(stmt).all()

def update_audit(
    session: Session,
    protocol: str,
    version: str,
    company: str,
    audit_data: AuditUpdate
) -> Audit | None:
    audit = get_audit(session, protocol, version, company)
    if not audit:
        return None

    audit.url = audit_data.url
    audit.last_updated = datetime.now()
    
    session.add(audit)
    session.commit()
    session.refresh(audit)
    return audit
