from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from core.database import get_session
from models.source_code import (
    SourceCodeCreate,
    SourceCodeUpdate,
    SourceCodeResponse,
    SourceCodeListResponse,
)
from schemas.response import ErrorResponse
import crud.source_code

router = APIRouter(
    prefix="/source-code",
    tags=["source_code"],
)

@router.post(
    "/",
    response_model=SourceCodeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid input data"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Create a new source code entry",
)
def create_source_code(
    *,
    session: Session = Depends(get_session),
    source_code_in: SourceCodeCreate,
) -> Any:
    """Create new source code entry"""
    source_code = crud.source_code.create_source_code(session, source_code_in)
    return source_code

@router.get(
    "/{source_code_id}",
    response_model=SourceCodeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Source code not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Get source code by ID",
)
def read_source_code(
    *,
    session: Session = Depends(get_session),
    source_code_id: int,
) -> Any:
    """Get source code by ID"""
    source_code = crud.source_code.get_source_code(session, source_code_id)
    if not source_code:
        raise HTTPException(status_code=404, detail="Source code not found")
    return source_code

@router.get(
    "/",
    response_model=SourceCodeListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="List source code entries",
)
def list_source_codes(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=100, lte=100),
    protocol: Optional[str] = None,
    version: Optional[str] = None,
) -> Any:
    """List source code entries with optional filters"""
    source_codes = crud.source_code.get_source_codes(
        session=session,
        skip=skip,
        limit=limit,
        protocol=protocol,
        version=version
    )
    return {
        "total": len(source_codes),
        "items": source_codes
    }

@router.put(
    "/{source_code_id}",
    response_model=SourceCodeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Source code not found"
        },
        400: {
            "model": ErrorResponse,
            "description": "Invalid input data"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Update source code entry",
)
def update_source_code(
    *,
    session: Session = Depends(get_session),
    source_code_id: int,
    source_code_in: SourceCodeUpdate,
) -> Any:
    """Update source code entry"""
    source_code = crud.source_code.update_source_code(
        session, source_code_id, source_code_in
    )
    if not source_code:
        raise HTTPException(status_code=404, detail="Source code not found")
    return source_code

@router.delete(
    "/{source_code_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Source code not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        },
    },
    summary="Delete source code entry",
)
def delete_source_code(
    *,
    session: Session = Depends(get_session),
    source_code_id: int,
):
    """Delete source code entry"""
    if not crud.source_code.delete_source_code(session, source_code_id):
        raise HTTPException(status_code=404, detail="Source code not found")
