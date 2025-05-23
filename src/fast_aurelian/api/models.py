from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for paper queries."""

    query: str = Field(..., description="The question to ask")
    max_sources: int | None = Field(default=5, description="Maximum number of sources to include")
    include_summary: bool | None = Field(default=True, description="Include summary in response")


class SearchRequest(BaseModel):
    """Request model for paper search."""

    search_term: str = Field(..., description="Term to search for")
    limit: int | None = Field(default=10, ge=1, le=100, description="Maximum number of results")


class AddPaperRequest(BaseModel):
    """Request model for adding papers."""

    url: str | None = Field(default=None, description="URL of the paper")
    doi: str | None = Field(default=None, description="DOI of the paper")
    file_path: str | None = Field(default=None, description="Local file path")
    title: str | None = Field(default=None, description="Paper title")
    authors: list[str] | None = Field(default=None, description="List of authors")


class IndexRequest(BaseModel):
    """Request model for indexing papers."""

    directory: str | None = Field(default=None, description="Directory containing papers to index")
    recursive: bool | None = Field(default=True, description="Search subdirectories")
    file_types: list[str] | None = Field(default=["pdf"], description="File types to include")


# Response Models
class PaperSource(BaseModel):
    """Model for paper source information."""

    title: str
    authors: list[str]
    doi: str | None = None
    url: str | None = None
    year: int | None = None
    excerpt: str | None = None


class QueryResponse(BaseModel):
    """Response model for paper queries."""

    answer: str
    sources: list[PaperSource]
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    """Response model for paper search."""

    results: list[PaperSource]
    metadata: dict[str, Any]


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

    papers: list[PaperSource]
    total: int
    work_directory: str
