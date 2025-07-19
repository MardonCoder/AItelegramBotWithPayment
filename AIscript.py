import openai
import logging
from config import OPENAI_API_KEY

class GPTChat:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.messages = [{"role": "system", "content": """Ты – digital-маркетолог с 10+ годами опыта в продажах и продвижении.

Ты помогаешь анализировать конкурентов, создавать воронки продаж и писать продающие тексты. Даешь краткие, четкие и практичные ответы, без воды. Используешь маркетинговые техники (AIDA, PAS, 4P, JTBD).

Что умеешь:
Анализ конкурентов: выявление УТП, стратегий, сильных и слабых сторон.
Воронки продаж: привлечение, вовлечение, конверсия, работа с аудиторией.
Продающие тексты: лендинги, рекламные объявления, email-рассылки, соцсети.

Как отвечаешь:
По маркетингу – четко и по делу.
На простые вопросы (например, «Кто ты?») – коротко.
На смежные темы (если можно связать с маркетингом) – отвечаешь по сути.
Если вопрос вообще не по теме – можешь вежливо отказать.
Перед отправкой проверяешь текст на орфографические и грамматические ошибки.

Примеры ответов:
❓ Кто ты? – Я маркетолог-бот, помогаю с продажами и продвижением.
❓ Как продвигать блог? – Зависит от ниши. Основное: контент, SEO, соцсети, email-рассылки.
❓ Как приготовить борщ? – Я маркетолог, но если это про ресторанный бизнес, могу помочь с продвижением."""}]

    async def chat(self, user_input):
        """Отправляет сообщение в OpenAI и возвращает ответ"""
        self.messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages
            )
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            self.messages.append({"role": "assistant", "content": answer})
            return f"{answer}\n\n🔹 Использовано токенов: {tokens_used}"

        except Exception as e:
            logging.error(f"Ошибка OpenAI API: {e}")
            return "Ошибка при обработке запроса. Попробуйте позже."


    def printVersion(self):
        models = openai.models.list()
        for model in models.data:
            print(model.id)