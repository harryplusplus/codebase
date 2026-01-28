from pathlib import Path
import chromadb
import ollama
from chromadb import Documents, EmbeddingFunction, Embeddings
import typer

class OllamaEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            response = ollama.embed(
                model='nomic-embed-text-v2-moe',
                input=f'search_document: {text}'
            )
            embeddings.append(response['embeddings'][0])
        return embeddings

client = chromadb.PersistentClient()

collection = client.get_or_create_collection(
    name="codebase",
    embedding_function=OllamaEmbeddingFunction()
)

app = typer.Typer()

@app.command()
def init(paths: list[Path] = typer.Argument(..., help="Directories to index")):
    """Index all code files from directories (deletes and recreates DB)"""
    print(paths)


if __name__ == "__main__":
    app()
