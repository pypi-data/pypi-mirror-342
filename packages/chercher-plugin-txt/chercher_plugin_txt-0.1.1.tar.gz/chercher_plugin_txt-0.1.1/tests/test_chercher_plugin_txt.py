from chercher_plugin_txt import ingest
from chercher import Document

CONTENT = "Hello, world"


def test_valid_file(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text(CONTENT)

    uri = p.as_uri()
    documents = ingest(uri=uri)
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.uri == uri
        assert doc.body == CONTENT


def test_invalid_file(tmp_path):
    p = tmp_path / "test.md"
    p.write_text(CONTENT)

    uri = p.as_uri()
    documents = ingest(uri=uri)
    assert list(documents) == []


def test_missing_file(tmp_path):
    p = tmp_path / "missingno.txt"
    documents = ingest(uri=p.as_uri())
    assert list(documents) == []


def test_invalid_uri():
    uri = "https://files/file.txt"
    documents = ingest(uri=uri)
    assert list(documents) == []
