
import os
import json
import time
import requests
from datetime import datetime

def send_to_telegram(bot_token, chat_id, message, file_path=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        requests.post(url, data=data)
        if file_path and os.path.exists(file_path):
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            with open(file_path, "rb") as f:
                files = {"document": f}
                data = {"chat_id": chat_id}
                requests.post(url, data=data, files=files)
    except Exception as e:
        print("Telegram error:", e)

def backup_files(bot_token, chat_id, watch_paths):
    already_sent = set()
    while True:
        for path in watch_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for name in files:
                        file_path = os.path.join(root, name)
                        if file_path not in already_sent:
                            send_to_telegram(bot_token, chat_id, f"New file: {file_path}", file_path)
                            already_sent.add(file_path)
        time.sleep(10)
