import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

QUESTION_FILE = "questions.txt"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=data)
    print(response.text)


def load_questions():
    if not os.path.exists(QUESTION_FILE):
        return []

    with open(QUESTION_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    questions = content.split("\n---\n")
    return questions


def get_today_question():
    questions = load_questions()

    if len(questions) == 0:
        return "❌ No questions found."

    index_file = "index.txt"

    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            index = int(f.read())
    else:
        index = 0

    question = questions[index]

    index += 1

    if index >= len(questions):
        index = 0

    with open(index_file, "w") as f:
        f.write(str(index))

    return question
    def build_message(question):
    return (
        "📚 <b>MPSC Daily Quiz</b>\n\n"
        f"{question}\n\n"
        "━━━━━━━━━━━━━━━\n"
        "📢 Join our Telegram channel for more daily MPSC questions!"
    )


def main():
    question = get_today_question()

    if question == "❌ No questions found.":
        send_message(question)
        return

    message = build_message(question)
    send_message(message)


if __name__ == "__main__":
    main()
