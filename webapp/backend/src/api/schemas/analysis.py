from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ContractDependenciesRequest(BaseModel):
    """Request model for contract dependencies analysis."""

    address: str = Field(..., description="Contract address to analyze")
    from_block: Optional[str] = Field(None, description="Start block")
    to_block: Optional[str] = Field(None, description="End block")

class Edge(BaseModel):
    source: str = Field(..., description="Source node address")
    target: str = Field(..., description="Target node address")
    types: Dict[str, int] = Field(
            ...,
            description="Types of calls between nodes with their counts. Keys: 'call', 'delegatecall', 'staticcall'"
        )
    # depth: int = Field(..., description="Depth of the edge in the dependency graph")


class ContractDependenciesResponse(BaseModel):
    """Response model for contract dependencies analysis."""

    address: str
    from_block: int
    to_block: int
    n_nodes: int
    n_matching_transactions: int
    nodes: Dict[str, str]
    edges: List[Edge] = Field(
        ...,
        description="List of edges in the dependency graph, each representing a call between contracts",
    )


class ContractRiskRequest(BaseModel):
    """Request model for contract risk analysis."""

    address: str = Field(..., description="Contract address to analyze")


class ContractRiskResponse(BaseModel):
    """Response model for contract risk analysis."""

    address: str
    risk_score: float = Field(
        ..., ge=0, le=100, description="Risk score from 0 to 100"
    )
    risk_factors: Dict[str, Any] = Field(
        ..., description="Detailed risk factors"
    )
    attestation: Dict[str, Any] = Field(
        ...,
        description="Attestation data",
    )   

