import requests
import json
from config.settings import OLLAMA_BASE_URL, LLM_MODEL, MAX_TOKENS


class LLMClient:
    def __init__(self):
        self.model_name = LLM_MODEL
        self.base_url = OLLAMA_BASE_URL

    def generate_response(self, prompt, context=None):
        if context:
            full_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Ты - ассистент по государственным закупкам. Ты помогаешь пользователям находить информацию.

ИНСТРУКЦИИ:
1. Используй информацию из контекста ниже для ответа на вопрос
2. Если информация из контекста полностью отвечает на вопрос - используй её
3. Если информация частично отвечает - ответь на основе того, что есть, и укажи что информация неполная
4. Если в контексте совсем нет информации - вежливо скажи об этом
5. Отвечай естественно и полезно
6. Будь дружелюбным и готовым помочь

КОНТЕКСТ ДЛЯ ОТВЕТА:
{context}

Теперь ответь на вопрос пользователя:<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{prompt}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""
        else:
            full_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Ты - ассистент по государственным закупкам. Отвечай на вопросы пользователей.
Если не знаешь ответа - вежливо скажи об этом и предложи задать другой вопрос.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{prompt}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "num_predict": MAX_TOKENS,
                    }
                },
                timeout=90
            )
            response.raise_for_status()
            result = response.json()
            return result["response"].strip()

        except Exception as e:
            print(f"Error generating response: {e}")
            return "Извините, произошла ошибка. Попробуйте задать вопрос еще раз."
