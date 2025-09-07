import requests
import json
from config.settings import OLLAMA_BASE_URL, LLM_MODEL, MAX_TOKENS


class LLMClient:
    def __init__(self):
        self.model_name = LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    def generate_response(self, prompt, context=None):
        if context:
            system_prompt = f"""
Ты — AI-агент площадки "РасЭлТорг".
Ты работаешь в секции закупок госкомпаний и госкорпораций по 223-ФЗ.
Твоя задача — давать точные и полезные ответы на вопросы пользователей.

Форматы вопросов:
1. Термин — объясни значение простыми словами.
2. Проблема — разберись в ситуации и предложи решение, ссылаясь на нормы 223-ФЗ.
3. Работа пользователя — подскажи, как действовать в системе или процессе.

Правила:
- Используй контекст ниже для ответа.
- Если информации хватает — отвечай чётко и полно.
- Если информации недостаточно — укажи это и предложи, где можно найти дополнительно.
- Пиши естественно, структурированно и по делу.

КОНТЕКСТ:
{context}
"""
        else:
            system_prompt = """
Ты — AI-агент площадки "РасЭлТорг".
Ты работаешь в секции закупок госкомпаний и госкорпораций по 223-ФЗ.
Отвечай на вопросы пользователей в одном из трёх режимов:
- Термин
- Проблема
- Работа пользователя

Если не знаешь ответа — честно скажи об этом и предложи уточнить вопрос.
"""

        # Формируем финальный промт
        full_prompt = f"""
SYSTEM:
{system_prompt}

USER:
{prompt}

ASSISTANT:
"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,   # ниже температура = более точные ответы
                        "top_p": 0.9,
                        "num_predict": MAX_TOKENS,
                    }
                },
                timeout=90
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()

        except Exception as e:
            print(f"Error generating response: {e}")
            return "Извините, произошла ошибка. Попробуйте задать вопрос еще раз."
