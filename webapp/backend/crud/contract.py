from sqlmodel import Session, select
from models.contract import Contract, ContractCreate
from typing import List
from datetime import datetime

def create_contract(session: Session, contract_data: ContractCreate) -> Contract:
    contract = Contract(**contract_data.model_dump())
    session.add(contract)
    session.commit()
    session.refresh(contract)
    return contract

def get_contract(session: Session, address: str) -> Contract | None:
    return session.exec(
        select(Contract).where(Contract.address == address)
    ).first()

def update_contract(session: Session, address: str, contract_data: ContractCreate) -> Contract | None:
    contract = get_contract(session, address)
    if not contract:
        return None
        
    for key, value in contract_data.model_dump().items():
        setattr(contract, key, value)
    contract.last_updated = datetime.now()
    
    session.commit()
    session.refresh(contract)
    return contract

def delete_contract(session: Session, address: str) -> bool:
    contract = get_contract(session, address)
    if not contract:
        return False
        
    session.delete(contract)
    session.commit()
    return True

def get_contracts(
    session: Session, 
    protocol: str | None = None, 
    version: str | None = None
) -> List[Contract]:
    stmt = select(Contract)
    
    if protocol:
        stmt = stmt.where(Contract.protocol == protocol)
    if version:
        stmt = stmt.where(Contract.version == version)
    
    return session.exec(stmt).all()