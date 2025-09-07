from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
import os

CHROMA_PATH = "./db_metadata_v5"


def initialize_rag():
    print("Инициализация RAG-ассистента с моделью qwen3:4b...")

    # Используем Qwen3:4B через Ollama
    model = OllamaLLM(
        model="qwen3:4b",
        temperature=0.2,
        num_ctx=4096,
        num_predict=512
    )

    # Эмбеддинги
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")

    # Загрузка базы Chroma
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Промпт (важно: {context} всегда должен быть в prompt_template)
    prompt_template = PromptTemplate.from_template("""
SYSTEM:
{system_prompt}

КОНТЕКСТ (используй только для справки, не цитируй дословно технические метки):
{context}

USER:
{question}

ASSISTANT:
""")

    document_chain = create_stuff_documents_chain(llm=model, prompt=prompt_template)

    return db, document_chain


def format_context(documents):
    """Форматирует контекст из документов для подстановки в промпт"""
    if not documents:
        return ""
    context_parts = []
    for i, doc in enumerate(documents):
        source = doc.metadata.get("source", "неизвестный источник")
        section = doc.metadata.get("law_section", doc.metadata.get("article", ""))
        part = f"[Источник {i+1}: {source} | {section}]\n{doc.page_content.strip()}"
        context_parts.append(part)
    return "\n\n---\n\n".join(context_parts)


def build_system_prompt(context_str: str) -> str:
    """Строит system_prompt для Qwen3:4b (без рассуждений, только готовый ответ)"""
    base = """
Ты — AI-ассистент площадки "РасЭлТорг".
Ты работаешь с госзакупками по 223-ФЗ.
Твоя задача — помогать пользователю разбираться в законе и в работе системы.

Форматы вопросов:
1. Термин — дай чёткое определение простыми словами.
2. Проблема — предложи решение с опорой на нормы 223-ФЗ.
3. Работа пользователя — объясни, как действовать в системе или процессе.

Правила:
- Давай сразу готовый ответ, не показывай ход рассуждений.
- Пиши коротко, ясно и структурированно.
- Используй только проверенные сведения из контекста или закона.
- Если информации недостаточно — скажи об этом прямо и предложи, где уточнить.
"""
    if context_str:
        return base + f"\nКОНТЕКСТ:\n{context_str}\n"
    else:
        return base

def main():
    try:
        db, document_chain = initialize_rag()

        # Проверка загрузки документов
        docs = db.get()
        num_docs = len(docs['documents']) if 'documents' in docs else 0
        print("Инициализация прошла успешно!")
        print(f"Загружено документов из Chroma: {num_docs}")
        print("=" * 50)
        print("-" * 50)

        chat_history = []

        while True:
            user_input = input("Вы: ").strip()
            if user_input.lower() in ['exit', 'выход']:
                print("До свидания!")
                break
            if not user_input:
                continue

            # Поиск релевантных чанков
            results = db.similarity_search(user_input, k=3)
            documents = [
                Document(page_content=doc.page_content, metadata=doc.metadata)
                for doc in results
            ]

            # Форматируем контекст
            context_str = format_context(documents)

            # Строим system_prompt
            system_prompt = build_system_prompt(context_str)

            # Входные данные для цепочки
            inputs = {
                "question": user_input,
                "system_prompt": system_prompt,
                "context": documents  # Обязательно для create_stuff_documents_chain
            }

            try:
                answer = document_chain.invoke(inputs)
                chat_history.append({"role": "human", "content": user_input})
                chat_history.append({"role": "assistant", "content": answer})

                print("\nАссистент:\n" + answer)
                print("-" * 50)
            except Exception as e:
                print(f"\nОшибка при обработке запроса: {str(e)}")
                print("-" * 50)
    except Exception as e:
        print(f"Ошибка при инициализации: {str(e)}")


if __name__ == "__main__":
    main()
