from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


# Request Models
class QueryRequest(BaseModel):
    """Request model for paper queries."""
    query: str = Field(..., description="The question to ask")
    max_sources: Optional[int] = Field(default=5, description="Maximum number of sources to include")
    include_summary: Optional[bool] = Field(default=True, description="Include summary in response")


class SearchRequest(BaseModel):
    """Request model for paper search."""
    search_term: str = Field(..., description="Term to search for")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Maximum number of results")


class AddPaperRequest(BaseModel):
    """Request model for adding papers."""
    url: Optional[str] = Field(default=None, description="URL of the paper")
    doi: Optional[str] = Field(default=None, description="DOI of the paper")
    file_path: Optional[str] = Field(default=None, description="Local file path")
    title: Optional[str] = Field(default=None, description="Paper title")
    authors: Optional[List[str]] = Field(default=None, description="List of authors")


class IndexRequest(BaseModel):
    """Request model for indexing papers."""
    directory: Optional[str] = Field(default=None, description="Directory containing papers to index")
    recursive: Optional[bool] = Field(default=True, description="Search subdirectories")
    file_types: Optional[List[str]] = Field(default=["pdf"], description="File types to include")


# Response Models
class PaperSource(BaseModel):
    """Model for paper source information."""
    title: str
    authors: List[str]
    doi: Optional[str] = None
    url: Optional[str] = None
    year: Optional[int] = None
    excerpt: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for paper queries."""
    answer: str
    sources: List[PaperSource]
    metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    """Response model for paper search."""
    results: List[PaperSource]
    metadata: Dict[str, Any]


class AddPaperResponse(BaseModel):
    """Response model for adding papers."""
    success: bool
    paper_id: str
    message: str


class IndexResponse(BaseModel):
    """Response model for indexing papers."""
    success: bool
    papers_indexed: int
    directory: str
    message: str


class ListPapersResponse(BaseModel):
    """Response model for listing papers."""
    papers: List[PaperSource]
    total: int
    work_directory: str