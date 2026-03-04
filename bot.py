import requests
import time
import re
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
THRESHOLD = 100000

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_site():
    response = requests.get("https://stake.com/sports")
    text = response.text

    amounts = re.findall(r"\$([0-9,]+\.\d+)", text)

    for amt in amounts:
        value = float(amt.replace(",", ""))
        if value > THRESHOLD:
            send_telegram(f"🚨 Whale Bet Detected: ${value:,.2f}")

while True:
    try:
        check_site()
    except Exception as e:
        print("Error:", e)

    time.sleep(60)
