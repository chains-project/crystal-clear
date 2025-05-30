from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.contract import Contract, ContractCreate
from models.audit import Audit
import crud.contract as crud
import crud.audit as audit_crud

class ContractService:
    def __init__(self, session: Session):
        self.session = session

    async def create_contract(self, contract_data: ContractCreate) -> Contract:
        try:
            return crud.create_contract(self.session, contract_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_contract(self, address: str) -> Contract:
        contract = crud.get_contract(self.session, address)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        return contract

    async def update_contract(self, address: str, contract_data: ContractCreate) -> Contract:
        contract = crud.update_contract(self.session, address, contract_data)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        return contract

    async def delete_contract(self, address: str) -> None:
        if not crud.delete_contract(self.session, address):
            raise HTTPException(status_code=404, detail="Contract not found")

    async def get_contracts(
        self, 
        protocol: str | None = None, 
        version: str | None = None
    ) -> list[Contract]:
        return crud.get_contracts(self.session, protocol, version)

    async def check_contract_audits(self, address: str) -> dict:
        contract = await crud.get_contract(self.session, address)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        audits = await audit_crud.get_audits(
            self.session,
            protocol=contract.protocol,
            version=contract.version
        )

        return {
            "contract": contract,
            "audits": audits
        }