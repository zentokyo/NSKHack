import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from core.search import HybridSearchAgent
from utils.file_processor import FileProcessor
from core.embedding import EmbeddingModel
from core.database import VectorDatabase
import argparse
import time


def initialize_database():
    print("Инициализация базы данных...")

    processor = FileProcessor()
    embedding_model = EmbeddingModel()
    vector_db = VectorDatabase(embedding_model)  # ✅ передаём модель

    print("Обработка Markdown файлов...")
    chunks, metadatas = processor.process_markdown_files("data/knowledge_base")

    if not chunks:
        print("Не найдено .md файлов для обработки")
        return

    print(f"Найдено {len(chunks)} чанков для обработки")

    print("Получение эмбеддингов...")
    batch_size = 3

    all_embeddings = []
    valid_chunks = []
    valid_metadatas = []

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        print(f"Обработка батча {i // batch_size + 1}/{(len(chunks) - 1) // batch_size + 1}")

        batch_embeddings = embedding_model.get_embeddings_batch(batch_chunks)

        for j, (chunk, embedding, metadata) in enumerate(
                zip(batch_chunks, batch_embeddings, metadatas[i:i + batch_size])):
            if embedding is not None and len(embedding) == 768:  # Проверяем размерность
                all_embeddings.append(embedding)
                valid_chunks.append(chunk)
                valid_metadatas.append(metadata)
                print(f"Чанк {i + j} - размерность {len(embedding)}")
            else:
                print(f"Чанк {i + j} - пропущен (None или неправильная размерность)")

        time.sleep(0.5)

    print(f"Успешно обработано {len(valid_chunks)} из {len(chunks)} чанков")

    if not valid_chunks:
        print("Нет валидных данных для добавления в базу")
        return

    print("Добавление документов в базу...")

    ids = [f"chunk_{i}" for i in range(len(valid_chunks))]

    vector_db.add_documents(
        documents=valid_chunks,
        metadatas=valid_metadatas,
        ids=ids,
        embeddings=all_embeddings
    )

    print("База данных успешно инициализирована!")


def interactive_mode():
    agent = HybridSearchAgent()
    print("=" * 60)
    print("Гибридный поисковый агент с llama3.2 запущен")
    print("Введите ваш вопрос (или 'quit' для выхода)")
    print("=" * 60)

    while True:
        try:
            query = input("\n🧠 Вопрос: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break

            if not query:
                continue

            print("Обработка запроса...")
            response = agent.process_query(query)
            print(f"\nОтвет: {response}")

        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent с гибридным поиском и llama3.2")
    parser.add_argument("--init", action="store_true", help="Инициализировать базу данных")
    parser.add_argument("--chat", action="store_true", help="Запустить интерактивный режим")

    args = parser.parse_args()

    if args.init:
        initialize_database()
    elif args.chat:
        interactive_mode()
    else:
        print("Используйте:")
        print("  --init   для инициализации базы")
        print("  --chat   для интерактивного режима")
