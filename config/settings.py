import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"

# Настройки ChromaDB
CHROMA_DB_PATH = BASE_DIR / "chroma_db"
CHROMA_COLLECTION_NAME = "knowledge_base"

# Настройки моделей
EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIMENSION = 768  # Размерность для nomic-embed-text
LLM_MODEL = "deepseek-r1:1.5b"

# Настройки Ollama
OLLAMA_BASE_URL = "http://localhost:11434"

# Настройки обработки текста
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Настройки генерации
MAX_TOKENS = 2000
TEMPERATURE = 0.1
TOP_P = 0.9

# Создаем директории если их нет
for directory in [CHROMA_DB_PATH, KNOWLEDGE_BASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)