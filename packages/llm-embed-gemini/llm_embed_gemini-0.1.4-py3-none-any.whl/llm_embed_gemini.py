from typing import Union, List, Iterable, Iterator, Optional

import llm
import urllib.request
import json
import os


@llm.hookimpl
def register_embedding_models(register):
    for model_id in (
            "gemini-embedding-exp-03-07",
            "text-embedding-004",
            "embedding-001"
    ):
        register(GeminiEmbeddingModel(model_id))


class GeminiEmbeddingModel(llm.EmbeddingModel):
    def __init__(self, model_id):
        self.model_id = model_id
        self._model = None
        self._gemini_api_key = os.getenv("GEMINI_API_KEY")
        self._task_type = "SEMANTIC_SIMILARITY"

    def embed(self, item: Union[str, bytes]) -> List[float]:
        # Endpoint URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-exp-03-07:embedContent?key={self._gemini_api_key}"

        # JSON payload
        data = {
            "model": f"models/{self.model_id}",
            "content": {
                "parts": [
                    {"text": item}
                ]
            },
            "taskType": self._task_type
        }

        json_data = json.dumps(data).encode("utf-8")

        # Create the request
        req = urllib.request.Request(
            url,
            data=json_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        # Send the request and read the response
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            embedding_values = result['embedding']['values']
            return embedding_values

    def embed_batch(self, items: Iterable[Union[str, bytes]]) -> List[List[float]]:
        raise NotImplementedError("Although the API supports chunking, it is not currently supported by this plugin.")

    def embed_multi(
            self, items: Iterable[Union[str, bytes]], batch_size: Optional[int] = None
    ) -> Iterator[List[float]]:
        raise NotImplementedError("Although the API supports chunking, it is not currently supported by this plugin.")
