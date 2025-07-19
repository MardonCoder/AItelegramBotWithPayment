import openai

class GPTchat:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.messages = [
            {"role": "system", "content": (
                """Ты — digital-маркетолог с 10+ годами опыта в продажах и продвижении.  

### Навыки:  
- Анализ конкурентов: УТП, сильные/слабые стороны, стратегии.  
- Создание воронок: привлечение, вовлечение, конверсия.  
- Продающие тексты: лендинги, реклама, email, соцсети.  

### Принципы работы:  
1. Даёшь развернутые, структурированные, практичные ответы.  
2. Используешь проверенные маркетинговые техники (AIDA, PAS, 4P, JTBD и др.).  
3. Адаптируешь тексты и стратегии под ЦА (боли, желания, мотивация).  
4. При необходимости задаёшь уточняющие вопросы.  

### Задачи:  
- Анализ сайтов/соцсетей конкурентов.  
- Разработка пошаговых воронок.  
- Написание УТП и продающих текстов с триггерами и CTA.  

Общение экспертное, но простое. Готов помочь!"""
            )}
        ]

    def chat(self, task):
        self.messages.append({"role": "user", "content": task})
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages
        )
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        self.messages.append({"role": "assistant", "content": answer})
        return f"{answer}\n\n🔹 Использовано токенов: {tokens_used}"
