import os
import json
import asyncio
from datetime import datetime, timedelta

from telegram import Bot
from telegram.constants import PollType

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
SHEET_ID = os.environ["SHEET_ID"]


creds = Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_CREDENTIALS"]),
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

bot = Bot(BOT_TOKEN)


# ---------- SETTINGS ----------

START_DATE = datetime(2026, 7, 1)

SHEET_NAME = "Sheet1"

QUESTIONS_PER_DAY = 10

# ------------------------------


def get_day_number():

    today = datetime.utcnow() + timedelta(hours=5, minutes=30)

    day = (today.date() - START_DATE.date()).days + 1

    if day < 1:
        day = 1

    return day


def get_questions(day):

    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:H"
    ).execute()

    rows = result.get("values", [])

    questions = []

    for row in rows:

        if len(row) < 8:
            continue

        if str(row[0]) == str(day):
            questions.append(row)

    return questions[:QUESTIONS_PER_DAY]


async def send_daily_quiz():

    day = get_day_number()

    questions = get_questions(day)

    if len(questions) == 0:

        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"❌ Day {day} साठी Google Sheet मध्ये प्रश्न उपलब्ध नाहीत."
        )

        return

    await bot.send_message(
        chat_id=CHAT_ID,
        text=(
            f"📚 MPSC COMBINE 2027\n\n"
            f"🗓 Day {day}\n"
            f"📝 आजची Quiz सुरू झाली आहे.\n\n"
            f"एकूण प्रश्न : {len(questions)}\n\n"
            f"शुभेच्छा! 🎯"
        )
    )

    for row in questions:

        question = row[1]

        options = [
            row[2],
            row[3],
            row[4],
            row[5]
        ]

        correct_option = int(row[6]) - 1

        explanation = row[7]

        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            type=PollType.QUIZ,
            correct_option_id=correct_option,
            is_anonymous=True,
            explanation=explanation,
            open_period=600
        )

        await asyncio.sleep(3)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "✅ आजची Quiz पूर्ण झाली.\n\n"
            "📚 उद्या दुपारी 3:00 वाजता पुढील Topic ची Quiz आपोआप येईल.\n\n"
            "🎯 All the Best!"
        )
    )


async def main():

    try:
        await send_daily_quiz()

    except Exception as e:

        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"❌ Bot Error:\n{e}"
        )

        raise


if __name__ == "__main__":
    asyncio.run(main())
