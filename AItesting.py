from testAIscript import GPTchat

from config import OPENAI_API_KEY

def main():
    chat_bot = GPTchat(OPENAI_API_KEY)
    print("Чат бот активирован! напишите exit для выхода")

    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            print("Чат завершён")
            break
        response = chat_bot.chat(user_input)
        print("Бот: ", response)

if __name__ == "__main__":
    main()