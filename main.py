from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
import os
import re

CHROMA_PATH = "./db_metadata_v5"


def clean_answer(text: str) -> str:
    """Удаляет скрытые рассуждения модели: теги <think>, <reasoning>, и фразы вроде 'Давайте подумаем'"""
    # Удаляем теги типа <think>...</think>
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<reasoning>.*?</reasoning>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Удаляем строки, начинающиеся с типичных фраз рассуждений
    lines = text.splitlines()
    filtered_lines = []
    skip_phrases = [
        "Давайте подумаем",
        "Рассмотрим",
        "Шаг 1",
        "Шаг 2",
        "Во-первых",
        "Во-вторых",
        "Итак,",
        "Таким образом,",
        "Хорошо,",
        "Понял,",
        "Я вижу,",
        "Проанализируем",
        "Обратим внимание",
        "Как видно из контекста",
        "На основе контекста",
        "Из предоставленного контекста",
        "Сначала",
        "Затем",
        "Наконец",
    ]

    for line in lines:
        if any(line.strip().startswith(phrase) for phrase in skip_phrases):
            continue  # Пропускаем строки с рассуждениями
        filtered_lines.append(line)

    # Собираем обратно и чистим пробелы
    text = "\n".join(filtered_lines).strip()

    # Дополнительно: удаляем пустые блоки в начале/конце
    text = re.sub(r"^\s*\n+", "", text)
    text = re.sub(r"\n+\s*$", "", text)

    return text


def initialize_rag():
    print("Инициализация RAG-ассистента с моделью qwen3:4b...")

    # Используем Qwen3:4B через Ollama — БЕЗ stop-токенов, чтобы не обрезать ответ
    model = OllamaLLM(
        model="qwen3:4b",
        temperature=0.2,
        num_ctx=4096,
        num_predict=2048
        # stop убран — чтобы не обрывать генерацию
    )

    # Эмбеддинги
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")

    # Загрузка базы Chroma
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Промпт
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
        part = f"[Источник {i + 1}: {source} | {section}]\n{doc.page_content.strip()}"
        context_parts.append(part)
    return "\n\n---\n\n".join(context_parts)


def build_system_prompt(context_str: str) -> str:
    """Строит system_prompt для Qwen3:4b — только готовый ответ, без рассуждений"""
    base = """
Ты — AI-консультант площадки "РасЭлТорг", специализирующийся на госзакупках по 223-ФЗ.
Твоя задача — помогать пользователям разбираться в законе и работе системы.

Форматы вопросов:
1. Термин — дай чёткое определение простыми словами.
2. Проблема — предложи решение с опорой на нормы 223-ФЗ.
3. Работа пользователя — объясни, как действовать в системе или процессе.

Правила:
- Никогда не показывай ход рассуждений. Не пиши фразы вроде "Давайте подумаем", "Шаг 1", "Как видно из контекста".
- Не используй теги  <think>, <reasoning> и им подобные — даже если хочется.
- Давай сразу готовый, структурированный и ясный ответ — как будто ты уже всё обдумал.
- Используй только проверенные сведения из контекста или закона.
- Если информации недостаточно — скажи об этом прямо и предложи, где уточнить.
- Ты консультант — отвечай доступно, но точно. Не добавляй лишнего.
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
                "context": documents
            }

            try:
                answer = document_chain.invoke(inputs)
                answer = clean_answer(answer)  # ← Здесь вырезаем всё лишнее

                if not answer.strip():
                    answer = "Извините, я не смог сформулировать ответ. Попробуйте переформулировать вопрос."

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