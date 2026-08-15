import requests
import os
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")
EMAIL_TO = os.environ.get("EMAIL_TO")
GVC_URL = os.environ.get("GVC_URL", "https://gvc.com.gr")
START_DATE = os.environ.get("START_DATE", "")
END_DATE = os.environ.get("END_DATE", "")

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=20)
        print("Telegram Alert Sent!")
    except Exception as e:
        print(f"Telegram failed: {e}")

def send_email(subject, body):
    try:
        plain_body = body.replace("<b>", "").replace("</b>", "")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(plain_body, 'plain'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"Email Sent to {EMAIL_TO}")
    except Exception as e:
        print(f"Email failed: {e}")

def check_gvc_slots():
    # === YAHAN AAPKA ASAL GVC CHECK LOGIC AAYEGA ===
    # Abhi ke liye False return kar raha hai
    # Aapne jo purana logic lagaya tha wo yahan paste karo
    try:
        return False, "No slot open"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    pk_time = datetime.now(pytz.timezone("Asia/Karachi"))
    time_str = pk_time.strftime('%d/%m/%Y %I:%M:%S %p')
    print(f"Checking at {time_str}...")

    found, reason = check_gvc_slots()
    
    if found:
        msg = f"""🇬🇷 <b>GREECE SLOT OPEN!</b> 🇬🇷
<b>Range:</b> {START_DATE} - {END_DATE}
<b>Reason:</b> {reason}
<b>Time:</b> {time_str}
<b>Link:</b> {GVC_URL}
Jaldi book karo!"""
        send_telegram(msg)
        send_email(f"🔥 GREECE SLOT FOUND - {time_str}", msg)
        print("SLOT FOUND - Alerts Sent!")
    else:
        # SLOT NAHI HAI TO KOI MESSAGE NAHI JAYEGA, SIRF LOG PRINT HOGA
        print(f"No slot: {reason} - No alert sent (this is final mode)")

if __name__ == "__main__":
    main()
