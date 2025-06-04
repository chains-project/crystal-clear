from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from models.repository import *

def create_repository(session: Session, repository: RepositoryCreate) -> Repository:
    db_repository = Repository(**repository.model_dump())
    session.add(db_repository)
    session.commit()
    session.refresh(db_repository)
    return db_repository

def get_repository(
    session: Session, 
    protocol: str,
    version: str
) -> Optional[Repository]:
    return session.get(Repository, {"protocol": protocol, "version": version})

def get_repositories(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    protocol: Optional[str] = None,
    version: Optional[str] = None
) -> List[Repository]:
    query = select(Repository)

    if protocol:
        query = query.where(Repository.protocol == protocol)
    if version:
        query = query.where(Repository.version == version)

    query = query.offset(skip).limit(limit)
    return session.exec(query).all()

def update_repository(
    session: Session, 
    protocol: str,
    version: str, 
    repository_update: RepositoryUpdate
) -> Optional[Repository]:
    db_repository = get_repository(session, protocol, version)
    if not db_repository:
        return None
    
    db_repository.url = repository_update.url
    db_repository.last_updated = datetime.now()
        
    session.add(db_repository)
    session.commit()
    session.refresh(db_repository)
    return db_repository

def delete_repository(
    session: Session, 
    protocol: str,
    version: str
) -> bool:
    db_repository = get_repository(session, protocol, version)
    if not db_repository:
        return False
    session.delete(db_repository)
    session.commit()
    return True