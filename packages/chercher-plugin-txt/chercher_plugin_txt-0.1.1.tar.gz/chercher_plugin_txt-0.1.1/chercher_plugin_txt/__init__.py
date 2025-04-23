from pathlib import Path
from typing import Generator
from chercher import Document, hookimpl


@hookimpl()
def ingest(uri: str) -> Generator[Document, None, None]:
    path = Path(uri).resolve()
    if not path.exists() or not path.is_file() or path.suffix != ".txt":
        return

    with path.open("r") as f:
        content = f.read()

    yield Document(uri=path.as_uri(), body=content, metadata={})
