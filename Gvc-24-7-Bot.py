import requests, os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EVENT = os.getenv("EVENT_NAME") # auto ya manual pata chalega

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg}, timeout=15)

print(f"Event: {EVENT} - Checking...")

try:
    r = requests.get("https://pk-gr-services.gvcworld.eu/", headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    text = r.text.lower()
    
    has_no_slot = "no slot" in text or "kein termin" in text or "keine termine" in text
    
    if not has_no_slot:
        send("🔥🔥🔥 GVC SLOT MIL GAYA BAYA! Jaldi kholo! https://pk-gr-services.gvcworld.eu/")
        print("SLOT FOUND - Message sent!")
    else:
        print("No slot")
        # Agar manual hai to bata do ke no slot hai
        if EVENT == "workflow_dispatch":
            send("✅ Manual check: Abhi koi slot nahi hai. Auto bot check karta rahega.")

except Exception as e:
    print(f"Error {e}")
    if EVENT == "workflow_dispatch":
        send(f"Manual check failed: {e}")
