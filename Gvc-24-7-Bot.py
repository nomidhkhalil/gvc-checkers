```python
import os
import requests
from datetime import datetime


# ============================================================
# TELEGRAM CONFIG
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EVENT_NAME = os.getenv("EVENT_NAME", "")


# ============================================================
# GVC URL
# ============================================================

GVC_URL = "https://pk-gr-services.gvcworld.eu/"


# ============================================================
# TELEGRAM SEND
# ============================================================

def send_telegram(message):
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN missing")
        return False

    if not CHAT_ID:
        print("❌ CHAT_ID missing")
        return False

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        response = requests.get(
            url,
            params={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=15
        )

        print(
            "Telegram status:",
            response.status_code
        )

        print(
            "Telegram response:",
            response.text
        )

        if response.ok:
            print("✅ Telegram message sent.")
            return True

        print("❌ Telegram message failed.")
        return False

    except Exception as e:
        print("❌ Telegram error:", e)
        return False


# ============================================================
# GVC CHECK
# ============================================================

def check_gvc():

    print()
    print("=" * 70)
    print("🇬🇷 GVC APPOINTMENT CHECKER")
    print("=" * 70)

    now = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    print("Time:", now)
    print("Event:", EVENT_NAME)
    print("URL:", GVC_URL)

    try:

        response = requests.get(
            GVC_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151.0 Safari/537.36"
                )
            },
            timeout=20
        )

        print(
            "HTTP status:",
            response.status_code
        )

        page = response.text.lower()

        # ----------------------------------------------------
        # Common unavailable messages
        # ----------------------------------------------------

        unavailable_phrases = [

            "no slot",
            "no slots",

            "no appointment",
            "no appointments",

            "not available",

            "appointment is not available",

            "there are no available",

            "please choose another date",

            "you cannot book an appointment on this date",

            "kein termin",
        ]

        unavailable = any(
            phrase in page
            for phrase in unavailable_phrases
        )

        # ----------------------------------------------------
        # Possible availability indicators
        # ----------------------------------------------------

        available_phrases = [

            "available slots",
            "appointment slots",
            "available appointment",
            "select time",
            "select slot",
            "choose time",
            "appointment time",
        ]

        available = any(
            phrase in page
            for phrase in available_phrases
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        if available and not unavailable:

            print()
            print("🟢🟢🟢 POSSIBLE SLOT FOUND 🟢🟢🟢")

            message = (
                "🔥🇬🇷 GVC APPOINTMENT ALERT!\n\n"
                "🟢 Possible appointment availability detected.\n\n"
                f"⏰ Time: {now}\n"
                f"🔗 {GVC_URL}\n\n"
                "⚠️ Please check the website manually."
            )

            send_telegram(message)

            return True

        if unavailable:

            print()
            print("🔴 NO APPOINTMENT SLOT DETECTED.")

            return False

        # ----------------------------------------------------
        # UNCLEAR RESULT
        # ----------------------------------------------------

        print()
        print("🟡 RESULT UNCLEAR.")

        print(
            "No clear availability message was detected."
        )

        return None

    except Exception as e:

        print()
        print("❌ GVC CHECK ERROR:")
        print(e)

        # Send error only for manual workflow
        # or if you specifically want error alerts.

        if EVENT_NAME == "workflow_dispatch":

            send_telegram(
                "⚠️ GVC Checker Error\n\n"
                f"{e}\n\n"
                f"🔗 {GVC_URL}"
            )

        return None


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("🚀 GVC CHECKER STARTED")
    print("=" * 70)

    result = check_gvc()

    print()
    print("=" * 70)

    if result is True:
        print("🟢 POSSIBLE APPOINTMENT DETECTED")

    elif result is False:
        print("🔴 NO SLOT DETECTED")

    else:
        print("🟡 RESULT UNCLEAR")

    print("=" * 70)
```
