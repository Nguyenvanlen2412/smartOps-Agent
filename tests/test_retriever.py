"""Retrieval quality evaluation against the real, persisted Chroma store.

Each case in eval_data/retrieval_eval_set.json pairs a realistic user query with
keywords drawn verbatim from the source docs in data/*.md. A "hit" means at least
one of a query's retrieved chunks contains one of its expected keywords. This
requires the vector store at ./chroma_db to already be populated (see
ingestion/vectorstore.py) and downloads the BAAI/bge-large-en-v1.5 embedding
model on first run.
"""

import json
from pathlib import Path

import pytest
from dotenv import load_dotenv

from rag.retriever import create_retriever

load_dotenv()

EVAL_SET_PATH = Path(__file__).parent / "eval_data" / "retrieval_eval_set.json"
EVAL_CASES = json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))

MIN_MRR = 0.5  # minimum acceptable mean reciprocal rank across the eval set


@pytest.fixture(scope="module")
def retriever():
    return create_retriever()


def _hit_rank(query: str, expected_keywords: list[str], retriever) -> int | None:
    """Return the 1-based rank of the first retrieved chunk matching a keyword, or None."""
    docs = retriever.invoke(query)
    for rank, doc in enumerate(docs, start=1):
        content = doc.page_content.lower()
        if any(keyword.lower() in content for keyword in expected_keywords):
            return rank
    return None


@pytest.mark.parametrize("case", EVAL_CASES, ids=[c["id"] for c in EVAL_CASES])
def test_retrieval_hit(case, retriever):
    """Every eval query should surface at least one relevant chunk within top-k."""
    rank = _hit_rank(case["query"], case["expected_keywords"], retriever)
    assert rank is not None, (
        f"No retrieved chunk contained any of {case['expected_keywords']!r} "
        f"for query: {case['query']!r}"
    )


def test_retrieval_mrr(retriever):
    """Aggregate mean reciprocal rank should stay above the regression threshold."""
    reciprocal_ranks = []
    misses = []
    for case in EVAL_CASES:
        rank = _hit_rank(case["query"], case["expected_keywords"], retriever)
        reciprocal_ranks.append(1 / rank if rank else 0)
        if rank is None:
            misses.append(case["id"])

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    print(f"\nRetrieval MRR@k: {mrr:.3f} over {len(EVAL_CASES)} queries")
    if misses:
        print(f"Missed queries: {misses}")

    assert mrr >= MIN_MRR, f"Retrieval MRR {mrr:.3f} fell below {MIN_MRR} threshold (misses: {misses})"
