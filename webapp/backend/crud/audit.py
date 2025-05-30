from sqlmodel import Session, select
from models.audit import Audit, AuditCreate
from typing import List

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

async def get_audits(session: Session, protocol: str = None, version: str = None, company: str = None) -> List[Audit]:
    stmt = select(Audit)
    
    if protocol:
        stmt = stmt.where(Audit.protocol == protocol)
    if version:
        stmt = stmt.where(Audit.version == version)
    if company:
        stmt = stmt.where(Audit.company == company)
    
    return session.exec(stmt).all()
