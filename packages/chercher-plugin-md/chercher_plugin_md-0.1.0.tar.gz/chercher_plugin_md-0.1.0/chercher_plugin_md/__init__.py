from pathlib import Path
from typing import Generator
import frontmatter
from chercher import Document, hookimpl


@hookimpl
def ingest(uri: str) -> Generator[Document, None, None]:
    path = Path(uri).resolve()
    if not path.exists() or not path.is_file() or path.suffix != ".md":
        return

    with path.open("r") as f:
        post = frontmatter.loads(f.read())

    yield Document(uri=path.as_uri(), body=post.content, metadata=post.metadata)
