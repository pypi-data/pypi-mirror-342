from metaso_sdk.model import Query
from metaso_sdk.search import search


def test_search():
    question = "42"
    query = Query(question=question)
    result = search(query)
    assert "resultId" in result
    assert "references" in result
    assert question in result["text"]


def test_search_stream():
    question = "42"
    query = Query(question=question)
    assert question in "".join(chunk["text"] for chunk in search(query, stream=True) if chunk["type"] == "append-text")
