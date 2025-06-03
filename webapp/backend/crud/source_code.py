from datetime import datetime
from typing import List, Optional, Tuple
from sqlmodel import Session, select
from models.source_code import SourceCode, SourceCodeCreate, SourceCodeUpdate

def create_source_code(session: Session, source_code: SourceCodeCreate) -> SourceCode:
    db_source_code = SourceCode(**source_code.model_dump())
    session.add(db_source_code)
    session.commit()
    session.refresh(db_source_code)
    return db_source_code

def get_source_code(
    session: Session, 
    protocol: str,
    version: str
) -> Optional[SourceCode]:
    return session.get(SourceCode, {"protocol": protocol, "version": version})

def get_source_codes(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    protocol: Optional[str] = None,
    version: Optional[str] = None
) -> List[SourceCode]:
    query = select(SourceCode)

    if protocol:
        query = query.where(SourceCode.protocol == protocol)
    if version:
        query = query.where(SourceCode.version == version)

    query = query.offset(skip).limit(limit)
    return session.exec(query).all()

def update_source_code(
    session: Session, 
    protocol: str,
    version: str, 
    source_code_update: SourceCodeUpdate
) -> Optional[SourceCode]:
    db_source_code = get_source_code(session, protocol, version)
    if not db_source_code:
        return None
    
    db_source_code.url = source_code_update.url
    db_source_code.last_updated = datetime.now()
        
    session.add(db_source_code)
    session.commit()
    session.refresh(db_source_code)
    return db_source_code

def delete_source_code(
    session: Session, 
    protocol: str,
    version: str
) -> bool:
    db_source_code = get_source_code(session, protocol, version)
    if not db_source_code:
        return False
    session.delete(db_source_code)
    session.commit()
    return True