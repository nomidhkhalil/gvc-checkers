import os, time, requests
from playwright.sync_api import sync_playwright
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GVC_EMAIL = os.getenv("GVC_EMAIL")
GVC_PASSWORD = os.getenv("GVC_PASSWORD")
GVC_URL = "https://pk-gr-services.gvcworld.eu/"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=15)
    print("Sent:", text[:100])

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(GVC_URL, timeout=60000)
            time.sleep(4)
            
            # Check if login form exists
            html = page.content()
            if "username" in html.lower() or "login" in html.lower():
                page.fill('input[type="text"], input[name="username"], input[name="email"], input[id="email"]', GVC_EMAIL)
                page.fill('input[type="password"]', GVC_PASSWORD)
                page.click('button[type="submit"]')
                page.wait_for_load_state("networkidle")
                time.sleep(6)
            
            after_login = page.content().lower()
            page_url = page.url
            
            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            if "dashboard" in after_login or "book appointment" in after_login or "logout" in after_login:
                msg = f"✅ <b>LOGIN SUCCESS!</b>\nTime: {now}\nURL: {page_url}\n\nBot andar pahunch gaya! Ab calendar check karna baaki hai."
            else:
                msg = f"⚠️ <b>Login ka pata nahi</b>\nTime: {now}\nURL: {page_url}\n\nPage ka text: {after_login[:500]}"
            
            send_telegram(msg)
            
        except Exception as e:
            send_telegram(f"❌ Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__": run()
