# PaperQA Indexing Strategy Plan

## Current Problem

The Fast-Aurelian API has inconsistent directory handling for PaperQA operations:

1. **`add_paper`**: Creates its own directory structure (e.g., "Attention Is All You Need/")
2. **`index_papers`**: Uses the specified directory (e.g., "../tests/papers")  
3. **`list_papers`**: Looks for index but can't find it due to directory mismatch
4. **Result**: Multiple separate `.pqa` indexes that don't communicate

## Current Behavior

```
add_paper(url) → Downloads to "Attention Is All You Need/" → Creates .pqa there
index_papers(dir) → Indexes "../tests/papers" → Creates separate .pqa there  
list_papers() → Looks for index but finds wrong/empty one
```

## Two Potential Strategies

### Strategy 1: Unified Central Index (Recommended)

**Concept**: All papers go into one central directory with one unified index.

**Benefits**:
- ✅ Single source of truth for all papers
- ✅ `list_papers` shows everything
- ✅ `query_papers` searches across all papers
- ✅ Simpler for users to understand
- ✅ Better for cross-paper analysis

**Implementation Steps**:
1. **Central Directory**: Define one main papers directory (e.g., `papers/`)
2. **Modify `add_paper`**: Always save to central directory, don't create subfolders
3. **Modify Service**: Ensure all operations use the same base directory
4. **Auto-organization**: Optionally organize by year/topic but keep in same index
5. **Migration**: Provide utility to merge existing scattered indexes

**API Changes**:
```python
# All operations work with the same base directory
POST /api/paperqa/add → Saves to papers/paper-title.pdf
POST /api/paperqa/index → Indexes papers/ directory  
GET /api/paperqa/list → Lists from unified index
POST /api/paperqa/query → Searches unified index
```

### Strategy 2: Distributed Multi-Index

**Concept**: Allow multiple separate indexes, but make them discoverable.

**Benefits**:
- ✅ Preserves current Aurelian behavior
- ✅ Allows topic-based organization  
- ✅ Supports project-specific collections

**Challenges**:
- ❌ More complex API
- ❌ Users need to manage multiple indexes
- ❌ Cross-collection search is harder

**Implementation Steps**:
1. **Index Registry**: Track all active indexes and their locations
2. **Collection Parameter**: Add `collection` parameter to all endpoints
3. **Auto-discovery**: Scan for existing `.pqa` folders  
4. **Multi-search**: Allow querying across multiple collections

## Recommended Approach: Strategy 1 (Unified Central Index)

### Phase 1: Fix Current Issues
1. **Service-level directory consistency**:
   ```python
   class PaperQAService:
       def __init__(self, base_directory="papers"):
           self.base_directory = Path(base_directory)
           # All operations use this base directory
   ```

2. **Fix `add_paper` to not create subfolders**:
   ```python
   # Instead of: "Attention Is All You Need/paper.pdf"  
   # Save as: "papers/attention-is-all-you-need.pdf"
   ```

3. **Consistent index location**:
   ```python
   # Always create .pqa in the base directory
   # papers/.pqa/ (not scattered across subdirectories)
   ```

### Phase 2: Enhanced Features
1. **Smart file naming**: Use DOI, title, or hash for unique filenames
2. **Metadata storage**: Store paper metadata in the index
3. **Duplicate detection**: Avoid adding the same paper twice
4. **Collection management**: Optional topic-based subfolders with unified search

### Phase 3: Advanced Features  
1. **Index merging**: Combine multiple existing indexes
2. **Export/import**: Backup and restore paper collections
3. **Search across collections**: Even with subfolders, search everything
4. **Web interface**: Visual management of papers and collections

## Implementation Priority

### High Priority (Fix Current Issues)
- [ ] Service-level directory consistency
- [ ] Fix `add_paper` folder creation
- [ ] Ensure single `.pqa` index location
- [ ] Update API to use consistent directories

### Medium Priority (Enhance UX)
- [ ] Smart file naming and organization  
- [ ] Duplicate detection
- [ ] Better error messages for index issues
- [ ] Index status endpoint

### Low Priority (Advanced Features)
- [ ] Multiple collection support
- [ ] Index merging utilities
- [ ] Web interface for management
- [ ] Export/import functionality

## Testing Strategy

1. **Integration tests**: Verify end-to-end workflow works
2. **Directory consistency tests**: Ensure all operations use same paths  
3. **Index persistence tests**: Verify index survives service restarts
4. **Multi-paper tests**: Add multiple papers and verify they're all searchable

## Current Status

- ✅ Environment setup fixed (PQA_HOME at startup)
- ✅ Index folders being created  
- ✅ Singleton service with @lru_cache
- ❌ Directory consistency still broken
- ❌ `list_papers` still returns 0 despite successful indexing

### Failing Integration Test

The integration test `test_paperqa_workflow` demonstrates the indexing problem:

```
Initial papers: 0
Add result: paper_directory='Attention Is All You Need', indexed_papers=['1706.03762.pdf']
Index result: paper_directory='../tests/papers', indexed_papers=['curate_gpt.pdf'] 
After adding: 0 papers  # ❌ Should be 1

# Logs show the problem:
- add_paper: "Building index for 1 documents in Attention Is All You Need"
- index_papers: "Building index for 1 documents in ../tests/papers"  
- list_papers: "No index found or index is empty"
```

**Root Cause**: Each operation uses different directories:
- `add_paper` creates `"Attention Is All You Need/"` directory 
- `index_papers` uses `"../tests/papers"` directory
- `list_papers` looks in yet another location

**Result**: Multiple isolated `.pqa` indexes that don't communicate.

## Next Steps

1. **URGENT**: Implement Phase 1 changes for directory consistency
2. Fix the failing integration test as validation
3. Test with integration test to verify all operations work together
4. Add proper error handling and user feedback
5. Document the unified approach in API docs