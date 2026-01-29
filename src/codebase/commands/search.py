import json
from typing import Any

import ollama

from codebase.constants import MODEL_NAME
from codebase.db import get_client, get_collection


def search_command(query: str, top_k: int):
    client = get_client()
    collection = get_collection(client)

    response = ollama.embed(model=MODEL_NAME, input=f"search_query: {query}")
    query_embedding = response["embeddings"][0]

    result = collection.query(
        query_embeddings=[query_embedding], n_results=top_k
    )
    documents = result["documents"] or [[]]
    metadatas = result["metadatas"] or [[]]
    distances = result["distances"] or [[]]

    output: list[dict[str, Any]] = []
    for i, (document, metadata, distance) in enumerate(
        zip(
            documents[0],
            metadatas[0],
            distances[0],
        )
    ):
        output.append(
            {
                "rank": i + 1,
                "file_path": metadata["file_path"],
                "distance": round(distance, 4),
                "content": document,
            }
        )

    print(json.dumps(output, indent=2, ensure_ascii=False))
