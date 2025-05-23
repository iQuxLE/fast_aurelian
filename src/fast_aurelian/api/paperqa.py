"""
FastAPI routes for PaperQA operations.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ..services.paperqa import PaperQAService

router = APIRouter(prefix="/api/paperqa", tags=["PaperQA"])


class PaperQuery(BaseModel):
    """Model for querying papers."""

    query: str = Field(..., description="The question to answer based on papers")


class PaperSearch(BaseModel):
    """Model for searching papers."""

    query: str = Field(..., description="The search query for finding papers")
    max_papers: int | None = Field(None, description="Maximum number of papers to return")


class PaperAdd(BaseModel):
    """Model for adding a paper."""

    path: str = Field(..., description="Path to the paper file or URL")
    citation: str | None = Field(None, description="Optional citation for the paper")


class DirectoryIndex(BaseModel):
    """Model for indexing a directory of papers."""

    directory: str | None = Field(None, description="Directory containing papers to index")


class AgentQuery(BaseModel):
    """Model for complex agent-based research queries."""

    query: str = Field(..., description="Complex research question for the agent to handle")
    context: str | None = Field(None, description="Additional context for the research")
    max_papers: int | None = Field(10, description="Maximum papers to consider")


from functools import lru_cache

@lru_cache()
def get_paperqa_service():
    """
    Dependency that provides a PaperQA service instance.
    
    Uses lru_cache to ensure the same service instance is reused,
    maintaining the index state across requests.

    Returns:
        Configured PaperQA service
    """
    return PaperQAService()


@router.post("/query", response_model=dict[str, Any])
async def query_papers(query: PaperQuery, service: PaperQAService = Depends(get_paperqa_service)):
    """
    Query papers to answer a specific question.

    This endpoint analyzes the papers in your collection to provide
    an evidence-based answer to your question.
    """
    try:
        result = await service.query_papers(query.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/search", response_model=dict[str, Any])
async def search_papers(
    search: PaperSearch, service: PaperQAService = Depends(get_paperqa_service)
):
    """
    Search for papers relevant to a query.

    This endpoint searches for scientific papers based on your query
    and returns the most relevant results.
    """
    try:
        result = await service.search_papers(search.query, search.max_papers)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/add", response_model=dict[str, Any])
async def add_paper(paper: PaperAdd, service: PaperQAService = Depends(get_paperqa_service)):
    """
    Add a paper to the collection.

    This endpoint adds a paper from a file path or URL to your collection
    for searching and querying.
    """
    try:
        result = await service.add_paper(paper.path, paper.citation)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/index", response_model=dict[str, Any])
async def index_papers(
    index_request: DirectoryIndex, service: PaperQAService = Depends(get_paperqa_service)
):
    """
    Index papers in a directory.

    This endpoint builds a search index for all papers in the specified directory.
    The index is required for searching and querying papers.
    """
    try:
        result = await service.index_papers(index_request.directory)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/list", response_model=dict[str, Any])
async def list_papers(
    directory: str | None = None, service: PaperQAService = Depends(get_paperqa_service)
):
    """
    List all papers in the collection.

    This endpoint returns a list of all papers in your collection along
    with their metadata.
    """
    try:
        result = await service.list_papers(directory)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
