import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import EmbeddingFunction
from config.settings import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME


class CustomEmbeddingFunction(EmbeddingFunction):
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def __call__(self, input):
        if isinstance(input, str):
            return [self.embedding_model.get_embedding(input)]
        return self.embedding_model.get_embeddings_batch(input)


class VectorDatabase:
    def __init__(self, embedding_model):
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_PATH),
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
            embedding_function=CustomEmbeddingFunction(embedding_model)
        )

    def add_documents(self, documents, metadatas, ids, embeddings):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

    def similarity_search(self, query, n_results=5):
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

    def hybrid_search(self, query_embedding, query_text, n_results=5):
        return self.similarity_search(query_text, n_results)
