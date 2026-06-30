import os
import json
import asyncio
from telegram import Bot
from telegram.constants import PollType
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
SHEET_ID = os.environ["SHEET_ID"]

creds = Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_CREDENTIALS"]),
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()
bot = Bot(BOT_TOKEN)


def get_questions():
    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range="Sheet1!A2:H11"
    ).execute()

    return result.get("values", [])
    async def send_quiz():
    questions = get_questions()

    for row in questions:
        if len(row) < 8:
            continue

        question = row[1]
        options = [row[2], row[3], row[4], row[5]]
        correct_option = int(row[6])

        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            type=PollType.QUIZ,
            correct_option_id=correct_option,
            is_anonymous=False,
            explanation=row[7],
        )

        await asyncio.sleep(30)
        async def send_quiz():
    questions = get_questions()

    for row in questions:
        if len(row) < 8:
            continue

        question = row[1]
        options = [row[2], row[3], row[4], row[5]]
        correct_option = int(row[6])

        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            type=PollType.QUIZ,
            correct_option_id=correct_option,
            is_anonymous=False,
            explanation=row[7],
        )

        await asyncio.sleep(30)
