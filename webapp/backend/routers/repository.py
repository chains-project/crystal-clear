from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from core.database import get_session
from models.repository import (
    RepositoryCreate,
    RepositoryUpdate,
    RepositoryResponse,
    RepositoryListResponse,
)
from schemas.response import ErrorResponse
import crud.repository as crud

router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)

@router.post(
    "/",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Create a new source repository entry",
)
def create_repository(
    *,
    session: Session = Depends(get_session),
    repository_in: RepositoryCreate,
) -> Any:
    """Create new source repository entry"""
    try:
        repository = crud.create_repository(session, repository_in)
        return repository
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Repository for protocol {repository_in.protocol} version {repository_in.version} already exists"
        )

@router.get(
    "/{protocol}/{version}",
    response_model=RepositoryResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Source repository not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get source repository by protocol and version",
)
def read_repository(
    *,
    session: Session = Depends(get_session),
    protocol: str,
    version: str,
) -> Any:
    """Get source repository by protocol and version"""
    repository = crud.get_repository(session, protocol, version)
    if not repository:
        raise HTTPException(status_code=404, detail="Source repository not found")
    return repository

@router.get(
    "/",
    response_model=RepositoryListResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="List source repository entries",
)
def list_repositories(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=100, lte=100),
    protocol: Optional[str] = None,
    version: Optional[str] = None,
) -> Any:
    """List source repository entries with optional filters"""
    repositories = crud.get_repositories(
        session=session,
        skip=skip,
        limit=limit,
        protocol=protocol,
        version=version
    )
    return {
        "total": len(repositories),
        "items": repositories
    }

@router.put(
    "/{protocol}/{version}",
    response_model=RepositoryResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Source repository not found"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Update source repository entry",
)
def update_repository(
    *,
    session: Session = Depends(get_session),
    protocol: str,
    version: str,
    repository_in: RepositoryUpdate,
) -> Any:
    """Update source repository entry"""
    repository = crud.update_repository(
        session, protocol, version, repository_in
    )
    if not repository:
        raise HTTPException(status_code=404, detail="Source repository not found")
    return repository

@router.delete(
    "/{protocol}/{version}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Source repository not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Delete source repository entry",
)
def delete_repository(
    *,
    session: Session = Depends(get_session),
    protocol: str,
    version: str,
) -> None:
    """Delete source repository entry"""
    if not crud.delete_repository(session, protocol, version):
        raise HTTPException(status_code=404, detail="Source repository not found")
