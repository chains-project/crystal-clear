from sqlmodel import Session

from core.exceptions import InputValidationError, InternalServerError
import crud.audit
from models.audit import AuditCreate, Audit, AuditUpdate

class AuditService:
    """
    Service for managing audits.
    Provides methods to create, delete, and retrieve audit entries.
    """

    def __init__(self, session: Session):
        self.session = session

    async def create_audit(self, audit_data: AuditCreate) -> AuditCreate:
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

            audit = crud.audit.create_audit(self.session, audit_data)
            return audit
        except Exception as e:
            raise InternalServerError(f"Failed to create audit: {str(e)}") from e

    async def delete_audit(self, id: int) -> bool:
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
            success = crud.audit.delete_audit(self.session, id)
            if not success:
                raise InternalServerError(f"Audit with ID {id} not found.")
            return True
        except Exception as e:
            raise InternalServerError(f"Failed to delete audit: {str(e)}") from e

    async def get_audit(self, id: int) -> Audit | None:
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
            audit = crud.audit.get_audit(self.session, id)
            if not audit:
                raise InternalServerError(f"Audit with ID {id} not found.")
            return audit
        except Exception as e:
            raise InternalServerError(f"Failed to get audit: {str(e)}") from e

    async def get_audits(
        self,
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
            audits = crud.audit.get_audits(self.session, protocol, version, company)
            return audits
        except Exception as e:
            raise InternalServerError(f"Failed to get audits: {str(e)}") from e

    async def update_audit(self, id: int, audit_data: AuditUpdate) -> Audit:
        """
        Update an existing audit entry.

        Args:
            session: SQLAlchemy session
            id: ID of the audit entry to update
            audit_data: New data for the audit entry

        Returns:
            Updated audit entry

        Raises:
            InputValidationError: If the input data is invalid
            InternalServerError: If the update fails
        """
        try:
            audit = crud.audit.update_audit(self.session, id, audit_data)
            if not audit:
                raise InternalServerError(f"Audit with ID {id} not found.")
            return audit
        except Exception as e:
            raise InternalServerError(f"Failed to update audit: {str(e)}") from e

