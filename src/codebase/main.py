from pathlib import Path
import chromadb
import ollama
from chromadb import Documents, EmbeddingFunction, Embeddings
import typer

from codebase.constants import COLLECTION_NAME, MODEL_NAME


class OllamaEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            response = ollama.embed(
                model=MODEL_NAME, input=f"search_document: {text}"
            )
            embeddings.append(response["embeddings"][0])
        return embeddings


client = chromadb.PersistentClient()

collection = client.get_or_create_collection(
    name=COLLECTION_NAME, embedding_function=OllamaEmbeddingFunction()
)

app = typer.Typer()


@app.command()
def init(paths: list[Path] = typer.Argument(..., help="Directories to index")):
    """Index all code files from directories (clears and recreates collection)."""

    try:
        client.delete_collection(COLLECTION_NAME)
        typer.secho("✓ Cleared existing collection.", fg=typer.colors.YELLOW)
    except Exception:
        pass


if __name__ == "__main__":
    app()
