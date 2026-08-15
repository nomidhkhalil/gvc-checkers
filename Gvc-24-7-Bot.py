import os, time, requests
from playwright.sync_api import sync_playwright
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GVC_EMAIL = os.getenv("GVC_EMAIL")
GVC_PASSWORD = os.getenv("GVC_PASSWORD")
GVC_URL = "https://pk-gr-services.gvcworld.eu/"

def send_telegram(text, photo_path=None):
    try:
        if photo_path:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            with open(photo_path, 'rb') as f:
                requests.post(url, data={"chat_id": CHAT_ID, "caption": text}, files={"photo": f}, timeout=20)
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except Exception as e: print(e)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(GVC_URL, timeout=60000)
            time.sleep(3)
            # USERNAME + PASSWORD LOGIN
            page.fill('input[type="text"], input[name="username"], input[name="email"]', GVC_EMAIL)
            page.fill('input[type="password"]', GVC_PASSWORD)
            page.click('button[type="submit"], button:has-text("Login")')
            page.wait_for_load_state("networkidle")
            time.sleep(5)
            print("Logged in with username")
            page.screenshot(path="screenshot.png")
            content = page.content().lower()
            no_slot = "no slot" in content or "fully booked" in content or "no appointment" in content
            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            if not no_slot:
                send_telegram(f"🇬🇷 <b>SLOT OPEN MAYBE!</b>\nTime: {now}\n{ GVC_URL }", "screenshot.png")
            else:
                send_telegram(f"⏰ <b>10 Min Check - Logged In</b>\nStatus: No slot\nTime: {now}", "screenshot.png")
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="error.png")
            send_telegram(f"⚠️ Error: {e}", "error.png")
        finally: browser.close()

if __name__ == "__main__": run()
