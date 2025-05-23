from fastapi.testclient import TestClient
from src.fast_aurelian.main import app
import tempfile
import shutil
from pathlib import Path


def test_paperqa_workflow():
    """Test the core PaperQA workflow: index → query → search."""
    client = TestClient(app)
    test_dir = "./tests/papers"
    Path(test_dir).mkdir(exist_ok=True)

    print("\n=== PaperQA Workflow Test ===")

    # 1. Index papers in directory
    print(f"\n1. Indexing papers in {test_dir}...")
    response = client.post("/api/paperqa/index", json={"directory": test_dir})
    print(f"Index result: {response.json()}")
    assert response.status_code == 200
    
    index_result = response.json()
    assert index_result["success"] == True
    assert index_result["indexed_chunks_count"] > 0  # Should have indexed something

    # 2. Query the indexed papers  
    print(f"\n2. Querying indexed papers...")
    response = client.post("/api/paperqa/query", 
                          json={"query": "What is this paper about?"})
    print(f"Query result: {response.json()}")
    assert response.status_code == 200
    
    query_result = response.json()
    # Should NOT get "No papers indexed" message if indexing worked
    assert "No papers are currently indexed" not in str(query_result)

    # 3. Search for new papers online
    print(f"\n3. Searching for new papers...")
    response = client.post("/api/paperqa/search",
                          json={"query": "machine learning", "max_papers": 2})
    print(f"Search result: {response.json()}")
    assert response.status_code == 200

    print("\n✅ Workflow test completed!")