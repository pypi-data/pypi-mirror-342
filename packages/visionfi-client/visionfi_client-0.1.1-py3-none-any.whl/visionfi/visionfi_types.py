"""Type definitions for the VisionFi client."""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    """Base model for API responses."""

    success: bool = True
    message: Optional[str] = None


class AnalyzeDocumentOptions(BaseModel):
    """Options for document analysis."""

    file_name: str
    analysis_type: str
    workflow_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AnalysisJob(BaseModel):
    """Representation of a document analysis job."""

    uuid: str
    status: str
    created_at: datetime
    client_id: str


class AnalysisResult(BaseModel):
    """Result of a document analysis job."""

    uuid: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class AuthVerificationResult(ApiResponse):
    """Result of authentication verification."""

    data: Union[Dict[str, Any], bool, Any] = Field(default_factory=dict)


class AuthTokenResult(ApiResponse):
    """Result of token retrieval."""

    data: Union[Dict[str, Any], str, Any] = Field(default_factory=dict)


class ClientFeature(BaseModel):
    """Client feature information."""

    name: str
    enabled: bool
    limits: Optional[Dict[str, Any]] = None


class ClientInfo(BaseModel):
    """Client account information."""

    client_id: str
    name: str
    status: str
    features: Dict[str, ClientFeature] = Field(default_factory=dict)
    created_at: datetime
    updated_at: Optional[datetime] = None


class ClientInfoResponse(ApiResponse):
    """Response containing client information."""

    data: Union[ClientInfo, Dict[str, Any], Any] = None


class WorkflowInfo(BaseModel):
    """Information about an analysis workflow."""

    workflow_key: str
    name: str
    description: str
    document_types: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)


class WorkflowsResponse(ApiResponse):
    """Response containing available workflows."""

    data: Union[List[WorkflowInfo], Dict[str, Any], List[Dict[str, Any]], Any] = Field(default_factory=list)