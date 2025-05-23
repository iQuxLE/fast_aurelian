from pathlib import Path

from aurelian.agents.paperqa import (
    PaperQADependencies,
    add_paper,
    get_config,
    paperqa_agent,
    query_papers,
)
from aurelian.agents.paperqa.paperqa_tools import (
    build_index,
    get_document_files,
    list_papers,
    search_papers,
)
from loguru import logger
from pydantic_ai import RunContext

AURELIAN_AVAILABLE = True
logger.info("Aurelian imports enabled")


class PaperQAService:
    """Service for interacting with Aurelian PaperQA tools and agent."""

    def __init__(self, default_paper_directory: str | None = None):
        """Initialize the PaperQA service with a default config."""
        if not AURELIAN_AVAILABLE:
            raise RuntimeError("Aurelian PaperQA components are not available")
        self.default_paper_directory = (
            Path(default_paper_directory) if default_paper_directory else Path.cwd() / "papers"
        )
        self.default_paper_directory.mkdir(exist_ok=True)
        
        self.config_deps: PaperQADependencies = get_config()
        self.config_deps.paper_directory = str(self.default_paper_directory)
        logger.info(f"Aurelian PaperQA config: {self.config_deps}")
        self.ctx = RunContext(deps=self.config_deps, model=None, usage=None, prompt=None)

    def _update_directory(self, paper_directory: str | None):
        """Update the config directory if different from default."""
        if paper_directory and paper_directory != str(self.default_paper_directory):
            target_dir = Path(paper_directory)
            target_dir.mkdir(exist_ok=True)
            self.config_deps.paper_directory = str(target_dir)
        else:
            self.config_deps.paper_directory = str(self.default_paper_directory)

    async def query_papers(self, query: str, paper_directory: str | None = None, **kwargs):
        """Query indexed papers to answer a question."""
        self._update_directory(paper_directory)

        if "max_sources" in kwargs:
            self.config_deps.answer_max_sources = kwargs["max_sources"]
        if "temperature" in kwargs:
            self.config_deps.temperature = kwargs["temperature"]
        if "evidence_k" in kwargs:
            self.config_deps.evidence_k = kwargs["evidence_k"]

        logger.info(f"Querying papers: {query} in {self.config_deps.paper_directory}")
        return await query_papers(self.ctx, query)

    async def search_papers(
        self, query: str, paper_directory: str | None = None, max_papers: int | None = None
    ):
        """Search for papers from the web and download them."""
        self._update_directory(paper_directory)
        return await search_papers(self.ctx, query, max_papers)

    async def add_paper(
        self,
        source: str,
        paper_directory: str | None = None,
        citation: str | None = None,
        auto_index: bool = True,
        **kwargs,
    ):
        """Add a single paper from URL or local path."""
        self._update_directory(paper_directory)
        return await add_paper(self.ctx, source, citation, auto_index)

    async def index_papers(self, paper_directory: str | None = None, **kwargs):
        """Index local PDF files in a directory."""
        self._update_directory(paper_directory)
        return await build_index(self.ctx)

    async def list_papers(self, paper_directory: str | None = None, **kwargs):
        """List papers in the collection."""
        self._update_directory(paper_directory)
        return await list_papers(self.ctx)

    async def run_agent(self, prompt: str, paper_directory: str | None = None, **kwargs):
        """Run the full PaperQA agent for complex operations."""
        self._update_directory(paper_directory)
        for key, value in kwargs.items():
            if hasattr(self.config_deps, key):
                setattr(self.config_deps, key, value)

        return await paperqa_agent.run(prompt, deps=self.config_deps)

    async def get_status(self, paper_directory: str | None = None):
        """Get status of paper collection."""
        target_dir = Path(paper_directory) if paper_directory else self.default_paper_directory

        try:
            doc_files = get_document_files(str(target_dir))
            paper_count = len(doc_files.get("all", [])) if doc_files else 0
            papers_found = doc_files.get("all", []) if doc_files else []
        except Exception:
            paper_count = 0
            papers_found = []

        return {
            "directory": str(target_dir),
            "directory_exists": target_dir.exists(),
            "paper_count": paper_count,
            "index_exists": (target_dir / ".pqa").exists(),
            "aurelian_available": AURELIAN_AVAILABLE,
            "papers_found": papers_found,
        }
