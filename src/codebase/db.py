from typing import Any

import chromadb
import ollama
from chromadb.api import ClientAPI

from codebase.constants import COLLECTION_NAME, MODEL_NAME


class OllamaEmbeddingFunction(chromadb.EmbeddingFunction[chromadb.Documents]):
    def __init__(self):
        pass

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        embeddings: list[Any] = []
        for text in input:
            response = ollama.embed(
                model=MODEL_NAME, input=f"search_document: {text}"
            )
            embeddings.append(response["embeddings"][0])
        return embeddings


def get_client() -> ClientAPI:
    return chromadb.PersistentClient(".codebase")


def get_collection(client: ClientAPI) -> chromadb.Collection:
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=OllamaEmbeddingFunction(),  # pyright: ignore[reportArgumentType]
    )
