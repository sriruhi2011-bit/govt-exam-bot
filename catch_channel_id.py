# catch_channel_id.py
"""
Listens for a message sent from your phone in the WhatsApp Channel
and automatically extracts the Channel ID (@newsletter) and saves it to my_keys.txt!
"""

import sys
import time
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from config.settings import WHATSAPP_INSTANCE_ID, WHATSAPP_API_TOKEN

def main():
    instance_id = WHATSAPP_INSTANCE_ID or "710722782267"
    token = WHATSAPP_API_TOKEN or "0a74b0b0192c487b8bc24d4a9d928ee0b077f1aec43949dba4"

    print("\n" + "=" * 65)
    print("   📡 WHATSAPP CHANNEL ID AUTO-DETECTOR")
    print("=" * 65)
    print("\n👉 ACTION REQUIRED ON YOUR PHONE:")
    print("   1. Open WhatsApp on your phone.")
    print("   2. Go to 'KanSiri Exam Prep' channel.")
    print("   3. Send ANY test message (e.g., 'Hello' or 'Test').")
    print("\n⏳ Listening for your channel post (waiting up to 90 seconds)...")

    recv_url = f"https://api.green-api.com/waInstance{instance_id}/receiveNotification/{token}"
    del_url = f"https://api.green-api.com/waInstance{instance_id}/deleteNotification/{token}"

    start_time = time.time()
    detected_id = None

    while time.time() - start_time < 90:
        try:
            res = requests.get(recv_url, timeout=10)
            if res.status_code == 200 and res.text.strip():
                data = res.json()
                receipt_id = data.get("receiptId")
                body = data.get("body", {})
                chat_id = (
                    body.get("senderData", {}).get("chatId")
                    or body.get("chatId")
                    or body.get("idMessage", "")
                )

                # Delete notification from queue so queue doesn't clog
                if receipt_id:
                    try:
                        requests.delete(f"{del_url}/{receipt_id}", timeout=5)
                    except:
                        pass

                # Check if this chat_id is a newsletter/channel or from KanSiri
                if chat_id:
                    print(f"   [Detected event] Chat ID: {chat_id}")
                    if "@newsletter" in chat_id:
                        detected_id = chat_id
                        break
                    elif "@" in chat_id:
                        # Keep it as candidate if newsletter was not found yet
                        candidate_id = chat_id
        except Exception as e:
            pass

        time.sleep(2)

    if detected_id:
        print("\n" + "🎉 " * 15)
        print(f"SUCCESS! Found your WhatsApp Channel ID:\n👉 {detected_id}")
        print("🎉 " * 15)

        # Automatically update my_keys.txt
        try:
            with open("my_keys.txt", "r", encoding="utf-8") as f:
                content = f.read()
            import re
            content = re.sub(r'WHATSAPP_CHAT_ID=.*', f'WHATSAPP_CHAT_ID={detected_id}', content)
            content = re.sub(r'WHATSAPP_ENABLED=.*', 'WHATSAPP_ENABLED=true', content)
            with open("my_keys.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("\n✅ Automatically saved to my_keys.txt!")
            print("   WHATSAPP_CHAT_ID=" + detected_id)
            print("   WHATSAPP_ENABLED=true")
        except Exception as err:
            print(f"Could not auto-update my_keys.txt: {err}")

        # Send test message to confirm
        print(f"\n📤 Sending test verification message to your channel...")
        test_url = f"https://api.green-api.com/waInstance{instance_id}/sendMessage/{token}"
        test_res = requests.post(test_url, json={
            "chatId": detected_id,
            "message": "🚀 *KanSiri Exam Prep Bot Connected Successfully!*\nDaily 360° Dossiers, Prelims Drills & Mains challenges will be posted here."
        }, timeout=15)
        if test_res.status_code == 200:
            print("✅ Verified! Check your WhatsApp Channel — the confirmation message has arrived!")
        else:
            print(f"Sent with response: {test_res.text}")
    else:
        print("\n⏳ Timed out waiting for channel message.")
        print("Please make sure you sent a message inside 'KanSiri Exam Prep' from your phone, then run this again:")
        print("   python catch_channel_id.py")

if __name__ == "__main__":
    main()
