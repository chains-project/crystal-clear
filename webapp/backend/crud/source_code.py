from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from models.source_code import SourceCode, SourceCodeCreate, SourceCodeUpdate

def create_source_code(session: Session, source_code: SourceCodeCreate) -> SourceCode:
    db_source_code = SourceCode.from_orm(source_code)
    session.add(db_source_code)
    session.commit()
    session.refresh(db_source_code)
    return db_source_code

def get_source_code(session: Session, source_code_id: int) -> Optional[SourceCode]:
    return session.get(SourceCode, source_code_id)

def get_source_codes(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    protocol: Optional[str] = None,
    version: Optional[str] = None
) -> List[SourceCode]:
    """
    Get source codes with optional protocol and version filters.
    
    Args:
        session: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        protocol: Optional protocol name to filter
        version: Optional version to filter
        
    Returns:
        List of matching SourceCode entries
    """
    query = select(SourceCode)

    # Add filters if provided
    if protocol:
        query = query.where(SourceCode.protocol == protocol)
    if version:
        query = query.where(SourceCode.version == version)

    # Add pagination
    query = query.offset(skip).limit(limit)
    
    return session.exec(query).all()

def update_source_code(
    session: Session, source_code_id: int, source_code_update: SourceCodeUpdate
) -> Optional[SourceCode]:
    db_source_code = get_source_code(session, source_code_id)
    if not db_source_code:
        return None
    
    source_code_data = source_code_update.model_dump(exclude_unset=True)
    for key, value in source_code_data.items():
        setattr(db_source_code, key, value)
    
    db_source_code.last_updated = datetime.now()
    session.add(db_source_code)
    session.commit()
    session.refresh(db_source_code)
    return db_source_code

def delete_source_code(session: Session, source_code_id: int) -> bool:
    db_source_code = get_source_code(session, source_code_id)
    if not db_source_code:
        return False
    session.delete(db_source_code)
    session.commit()
    return True