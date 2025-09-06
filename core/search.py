from .embedding import EmbeddingModel
from .database import VectorDatabase
from .llm import LLMClient
import time


class HybridSearchAgent:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_db = VectorDatabase(self.embedding_model)
        self.llm = LLMClient()

    def process_query(self, query):
        print(f"Обработка запроса: {query}")
        start_time = time.time()

        query_embedding = self.embedding_model.get_embedding(query)

        if not query_embedding:
            return "Не удалось обработать ваш вопрос. Попробуйте переформулировать."

        search_results = self.vector_db.hybrid_search(query_embedding, query, n_results=10)

        context = self._format_context(search_results, query)

        print(
            f"Найдено документов: {len(search_results['documents'][0]) if search_results and 'documents' in search_results else 0}"
        )

        response = self.llm.generate_response(query, context)

        return response

    def _format_context(self, search_results, query):
        if not search_results or 'documents' not in search_results or not search_results['documents'][0]:
            return f"По запросу '{query}' в базе знаний информация не найдена."

        documents = search_results['documents'][0]

        context_parts = ["ИНФОРМАЦИЯ ИЗ БАЗЫ ЗНАНИЙ:"]

        for i, doc in enumerate(documents[:5]):
            context_parts.append(f"\n--- Фрагмент {i + 1} ---\n{doc}")

        context_parts.append(f"\n\nВопрос пользователя: {query}")

        return "\n".join(context_parts)
