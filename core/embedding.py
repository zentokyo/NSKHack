import requests
import numpy as np
from config.settings import OLLAMA_BASE_URL, EMBEDDING_MODEL


class EmbeddingModel:
    def __init__(self):
        self.model_name = EMBEDDING_MODEL
        self.base_url = OLLAMA_BASE_URL

    def get_embedding(self, text):
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model_name,
                    "prompt": text
                }
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None

    def get_embeddings_batch(self, texts):
        return [self.get_embedding(text) for text in texts]