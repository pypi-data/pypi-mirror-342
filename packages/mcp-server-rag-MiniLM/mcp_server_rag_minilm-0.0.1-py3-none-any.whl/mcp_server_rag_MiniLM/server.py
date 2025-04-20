from mcp.server.fastmcp import FastMCP, Context
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from dataclasses import dataclass
from typing import TypedDict, List, Optional, Dict, Any
import json
import os
from pathlib import Path
import logging

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ----------------------------
# Chroma memory‑management settings (Section 2 of the optimisation)
# ----------------------------
# Default: 768 MB; override with the CHROMA_MEM_LIMIT_BYTES env var.
CHROMA_MEM_LIMIT_BYTES: int = int(os.getenv('CHROMA_MEM_LIMIT_BYTES', str(768 * 1024 ** 2)))


# ----------------------------
# Typing helpers
# ----------------------------

class SearchResult(TypedDict):
    document_number: int
    content: str
    metadata: Dict[str, Any]
    relevance: str
    distance_score: float

class SearchResponse(TypedDict):
    status: str
    query: str
    results: List[SearchResult]

# ----------------------------
# Config dataclass (unchanged functionality)
# ----------------------------
@dataclass
class ServerConfig:
    """Configuration for the RAG system that can be controlled through environment variables."""
    # Where ChromaDB will persist its data
    persist_dir: str = os.getenv('RAG_PERSIST_DIR', str(Path.home() / 'Documents/chroma_db'))
    # Path or name of the Sentence‑Transformer model
    embedding_model_name: str = os.getenv(
        'RAG_EMBEDDING_MODEL',
        str(Path.home() / 'LLM/huggingface/hub/models--sentence-...iniLM-L6-v2/snapshots/fa97f6e7cb1a59073dff9e6b13e2715cf7475ac9')
    )
    # Default number of results to return from searches
    n_results: int = int(os.getenv('RAG_N_RESULTS', '5'))
    # Memory limit to pass to Chroma (bytes)
    chroma_mem_limit_bytes: int = CHROMA_MEM_LIMIT_BYTES

# ----------------------------
# RAG Server setup
# ----------------------------
mcp = FastMCP('SAP Commerce RAG System')

class GlobalState:
    """Container for global state."""
    def __init__(self) -> None:
        self.embedding_model: Optional[SentenceTransformer] = None
        self.chroma_client: Optional[chromadb.PersistentClient] = None
        self.config: ServerConfig = ServerConfig()


state = GlobalState()

# ----------------------------
# Internal helpers
# ----------------------------

async def log_with_context(ctx: Context, message: str, level: str = 'info') -> None:
    """Log to the standard logger *and* the MCP context (if present)."""
    getattr(logger, level)(message)
    if ctx is not None:
        try:
            await getattr(ctx, level)(message)
        except Exception as e:  # pragma: no cover
            logger.error(f'Failed to log to context: {e}')


def _ensure_chroma_client() -> chromadb.PersistentClient:
    """Create the Chroma client once, with LRU segment-cache enabled (Section 2)."""
    if state.chroma_client is None:
        settings = Settings(
            anonymized_telemetry=False,
            chroma_segment_cache_policy='LRU',
            chroma_memory_limit_bytes=state.config.chroma_mem_limit_bytes,
        )
        state.chroma_client = chromadb.PersistentClient(
            path=state.config.persist_dir,
            settings=settings,
        )
    return state.chroma_client


def _get_collection(name: str) -> chromadb.Collection:
    """Return a Chroma collection handle *without* pinning it in global state (Section 3)."""
    client = _ensure_chroma_client()
    return client.get_or_create_collection(name=name)

async def initialize_services(collection_name: str, ctx: Optional[Context] = None) -> None:
    """Initialise embedding model and ensure the collection exists."""
    try:
        os.makedirs(state.config.persist_dir, exist_ok=True)
        if ctx:
            await log_with_context(ctx, f'Ensured data directory exists at {state.config.persist_dir}')

        # 1️⃣ Embedding model
        if state.embedding_model is None:
            state.embedding_model = SentenceTransformer(state.config.embedding_model_name)
            if ctx:
                await log_with_context(ctx, 'Embedding model loaded successfully')

        # 2️⃣ Chroma client + collection (created but NOT cached)
        _get_collection(collection_name)

    except Exception as e:
        error_msg = f'Initialization error: {e}'
        if ctx:
            await log_with_context(ctx, error_msg, 'error')
        raise RuntimeError(error_msg)

# ----------------------------
# Core retrieval logic
# ----------------------------

async def retrieve_context(
    query: str,
    collection_name: str,
    ctx: Context,
    n_results: Optional[int] = None,
) -> str:
    """Generic search function that works with any collection."""
    try:
        # Ensure model + client are available
        if state.embedding_model is None or state.chroma_client is None:
            await initialize_services(collection_name, ctx)

        logger.info('Encoding query and searching vector store…')

        # Generate query embedding
        query_embedding = state.embedding_model.encode([query], convert_to_numpy=True)

        # Perform vector search
        collection = _get_collection(collection_name)
        try:
            results = collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=n_results or state.config.n_results,
                include=['documents', 'metadatas', 'distances'],
            )
            logger.info(f'Query embedding shape: {query_embedding.shape}')
            logger.info(f'Number of results requested: {n_results or state.config.n_results}')
            logger.info(f'Raw ChromaDB response: {results}')
        except Exception as e:
            logger.error(f'ChromaDB query failed: {e}')
            return json.dumps({'status': 'error', 'message': f'Search operation failed: {e}'}, indent=2)

        # Validate response structure
        if not isinstance(results, dict) or 'documents' not in results:
            return json.dumps({'status': 'error', 'message': 'Invalid response format from database'}, indent=2)

        # Handle empty results
        if not results['documents'] or not results['documents'][0]:
            return json.dumps({'status': 'no_results', 'message': 'No relevant documents found for the query'}, indent=2)

        documents  = results.get('documents',  [[]])[0]
        metadatas  = results.get('metadatas', [[]])[0]
        distances  = results.get('distances', [[]])[0]

        context_entries: List[SearchResult] = []
        for i in range(len(documents)):
            relevance = ('High' if distances[i] < 0.5 else
                         'Medium' if distances[i] < 0.8 else
                         'Low')
            context_entries.append({
                'document_number': i + 1,
                'content': documents[i] if i < len(documents) else '',
                'metadata': metadatas[i] if i < len(metadatas) else {},
                'relevance': relevance,
                'distance_score': distances[i] if i < len(distances) else 0.0,
            })

        return json.dumps({'status': 'success', 'query': query, 'results': context_entries}, indent=2)

    except Exception as e:
        error_msg = f'Error during context retrieval: {e}'
        logger.error(error_msg)
        return json.dumps({'status': 'error', 'message': error_msg}, indent=2)


async def get_collection_info(collection_name: str, ctx: Context) -> str:
    """Return basic metadata (count, path, model) for a collection."""
    try:
        if state.embedding_model is None or state.chroma_client is None:
            await initialize_services(collection_name, ctx)

        collection = _get_collection(collection_name)
        doc_count = collection.count()

        return json.dumps({
            'status': 'success',
            'collection_name': collection_name,
            'document_count': doc_count,
            'persist_directory': state.config.persist_dir,
            'embedding_model': state.config.embedding_model_name,
            'is_initialized': state.embedding_model is not None and state.chroma_client is not None,
        }, indent=2)

    except Exception as e:
        error_msg = f'Error getting collection info: {e}'
        await log_with_context(ctx, error_msg, 'error')
        return json.dumps({'status': 'error', 'message': error_msg}, indent=2)

# ----------------------------
# MCP tools (API surface)
# ----------------------------

@mcp.tool()
async def retrieve_sap_comm_context(query: str, ctx: Context, n_results: Optional[int] = None) -> str:
    """Search for documents relevant to *query* in the sap‑commerce collection."""
    collection_name = 'sap-comm-rag'
    return await retrieve_context(query, collection_name, ctx, n_results)


@mcp.tool()
async def get_sap_comm_collection_info(ctx: Context) -> str:
    """Return stats for the sap‑commerce collection."""
    collection_name = 'sap-comm-rag'
    return await get_collection_info(collection_name, ctx)


async def cleanup_resources(ctx: Context) -> str:
    """Release embedding model + Chroma client (helpful in constrained environments)."""
    try:
        await log_with_context(ctx, 'Starting cleanup of RAG system resources…')

        # Drop references; GC + Chroma LRU will do the rest
        state.embedding_model = None
        if state.chroma_client is not None:
            try:
                state.chroma_client.close()  # Graceful shutdown in newer Chroma versions
            except Exception:  # pragma: no cover
                pass
        state.chroma_client = None

        await log_with_context(ctx, 'Cleanup complete')
        return json.dumps({'status': 'success', 'message': 'Resources cleaned up successfully'}, indent=2)

    except Exception as e:
        error_msg = f'Error during cleanup: {e}'
        await log_with_context(ctx, error_msg, 'error')
        return json.dumps({'status': 'error', 'message': error_msg}, indent=2)

def main():
    # Start the MCP server
    mcp.run()

if __name__ == '__main__':
    main()
