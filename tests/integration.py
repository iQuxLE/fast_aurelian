from fastapi.testclient import TestClient
from src.fast_aurelian.main import app
import tempfile
import shutil
from pathlib import Path


def test_paperqa_workflow():
    """Test the complete PaperQA workflow."""
    client = TestClient(app)
    test_dir = "../tests/papers"
    Path(test_dir).mkdir(exist_ok=True)

    # 1. Check initial state
    response = client.get("/api/paperqa/list")
    initial_data = response.json()
    print(f"Initial state: {initial_data}")

    # 2. Add a paper (downloads file)
    response = client.post("/api/paperqa/add",
                           json={"path": "https://arxiv.org/pdf/1706.03762.pdf",
                                 "citation": "Attention Is All You Need"})
    add_result = response.json()
    print(f"Add result: {add_result}")

    # 3. Check raw files in directory (should have +1 file)
    pdf_files = list(Path(test_dir).glob("*.pdf"))

    client = TestClient(app)
    response = client.get("/api/paperqa/list")
    initial_count = response.json().get("paper_count", 0)
    print(f"Initial papers: {initial_count}")

    test_dir = "../tests/papers"
    if not Path(test_dir).is_dir():
        Path(test_dir).mkdir(exist_ok=True)

    response = client.post("/api/paperqa/index",
                           json={"directory": test_dir})
    print(f"Index result: {response.json()}")
    #
    # 3. Add a paper
    response = client.post("/api/paperqa/add",
                           json={"path": "https://arxiv.org/pdf/1706.03762.pdf",
                                 "citation": "Attention Is All You Need"})
    print(f"Add paper result: {response.json()}")
    #
    # 4. Check list again (should have +1 paper)
    response = client.get("/api/paperqa/list")
    new_count = response.json().get("paper_count", 0)
    print(f"After adding: {new_count} papers")
    assert new_count == initial_count + 1

    # 5. Re-index to include the new paper
    response = client.post("/api/paperqa/index",
                           json={"directory": test_dir})
    print(f"Re-index result: {response.json()}")

    # 6. Now query should work with indexed papers
    response = client.post("/api/paperqa/query",
                           json={"query": "What is attention mechanism?"})
    print(f"Query result: {response.json()}")
    assert response.status_code == 200

    # 7. Search for more papers
    response = client.post("/api/paperqa/search",
                           json={"query": "transformer neural networks",
                                 "max_papers": 3})
    print(f"Search result: {response.json()}")


# Run the workflow
test_paperqa_workflow()