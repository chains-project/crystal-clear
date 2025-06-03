from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.contract import Contract, ContractCreate, ContractUpdate
import crud.contract as crud
import crud.audit as audit_crud
import crud.source_code as source_code_crud
from schemas.contract import ContractAuditCreate, ContractSourceCodeCreate
from models.audit import AuditCreate
from models.source_code import SourceCodeCreate

class ContractService:
    def __init__(self, session: Session):
        self.session = session

    async def create_contract(self, contract_data: ContractCreate) -> Contract:
        """Create a new contract"""
        try:
            return crud.create_contract(self.session, contract_data)
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Contract with address {contract_data.address} already exists"
            )

    async def get_contract(self, address: str) -> Contract:
        """Get contract by address"""
        contract = crud.get_contract(self.session, address)
        if not contract:
            raise HTTPException(
                status_code=404, 
                detail=f"Contract with address {address} not found"
            )
        return contract

    async def update_contract(self, address: str, contract_data: ContractUpdate) -> Contract:
        """Update contract by address"""
        contract = crud.update_contract(self.session, address, contract_data)
        if not contract:
            raise HTTPException(
                status_code=404, 
                detail=f"Contract with address {address} not found"
            )
        return contract

    async def delete_contract(self, address: str) -> None:
        """Delete contract by address"""
        if not crud.delete_contract(self.session, address):
            raise HTTPException(
                status_code=404, 
                detail=f"Contract with address {address} not found"
            )

    async def get_contracts(
        self, 
        protocol: str | None = None, 
        version: str | None = None
    ) -> list[Contract]:
        """Get contracts with optional protocol and version filters"""
        return crud.get_contracts(self.session, protocol, version)

    async def get_contract_audits(self, address: str) -> dict:
        """Check if contract has associated audits"""
        contract = await self.get_contract(address)
        
        audits = audit_crud.get_audits(
            self.session,
            protocol=contract.protocol,
            version=contract.version
        )

        return {
            "contract": contract,
            "audits": audits
        }
    
    async def get_contract_source_code(self, address: str) -> dict:
        """Get source code for a contract by address"""
        contract = await self.get_contract(address)
        
        source_code = source_code_crud.get_source_code(
            self.session,
            protocol=contract.protocol,
            version=contract.version
        )

        if not source_code:
            raise HTTPException(
                status_code=404, 
                detail=f"Source code for contract {address} not found"
            )

        return {
            "contract": contract,
            "source_code": source_code
        }
    
    async def add_contract_audit(self, address: str, audit_data: ContractAuditCreate) -> dict:
        """Add audit for a contract"""
        contract = await self.get_contract(address)
        
        try:
            # Create new audit
            audit_create = AuditCreate(
                protocol=contract.protocol,
                version=contract.version,
                company=audit_data.company,
                url=audit_data.url
            )
            
            audit = audit_crud.create_audit(self.session, audit_create)
            
            return {
                "contract": contract,
                "audits": [audit]
            }
        except IntegrityError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e.orig)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    async def add_contract_source_code(self, address: str, source_data: ContractSourceCodeCreate) -> dict:
        """Add source code for a contract"""
        contract = await self.get_contract(address)
        
        try:
            # Create new source code
            source_create = SourceCodeCreate(
                protocol=contract.protocol,
                version=contract.version,
                url=source_data.url
            )
            
            source = source_code_crud.create_source_code(self.session, source_create)
            
            return {
                "contract": contract,
                "source_code": source
            }
        except IntegrityError as e:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail=str(e.orig)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail= "Internal server error: " + str(e)
            )