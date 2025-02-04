import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


class TelegramBot:
    def __init__(self, token=TOKEN, chat_id=CHAT_ID):
        self.token = token
        self.chat_id = chat_id

    def send_notification(self, message: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("✅ Notificação enviada com sucesso!")
        else:
            print(f"❌ Erro ao enviar notificação: {response.text}")
