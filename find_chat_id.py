# find_chat_id.py
"""
Helper script to list all WhatsApp chats, groups, and channels connected
to your Green API instance, along with their exact Chat IDs.
"""

import os
import sys
import base64
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from config.settings import WHATSAPP_INSTANCE_ID, WHATSAPP_API_TOKEN


def main():
    instance_id = WHATSAPP_INSTANCE_ID
    token = WHATSAPP_API_TOKEN

    if not instance_id or not token:
        print("Please enter your Green API credentials:")
        instance_id = input("Instance ID: ").strip()
        token = input("API Token: ").strip()

    if not instance_id or not token:
        print("Error: Instance ID and API Token are required.")
        return

    print(f"\n🔍 Checking Green API Instance: {instance_id}...")

    # Step 1: Check authorization state
    state_url = f"https://api.green-api.com/waInstance{instance_id}/getStateInstance/{token}"
    try:
        s_res = requests.get(state_url, timeout=15)
        state_data = s_res.json() if s_res.status_code == 200 else {}
        state = state_data.get("stateInstance", "unknown")
    except Exception as e:
        print(f"Error connecting to Green API: {e}")
        return

    print(f"   Instance status: '{state}'")

    if state != "authorized":
        print("\n" + "⚠️ " * 15)
        print("YOUR INSTANCE IS NOT LINKED TO WHATSAPP YET!")
        print("⚠️ " * 15)
        print("\nTo link your WhatsApp:")
        print("1. Go to your Green API Console: https://console.green-api.com/")
        print("2. Open your instance and click 'QR code'")
        print("3. On your phone: Open WhatsApp -> Settings -> Linked Devices -> Link a Device")
        print("4. Scan the QR code displayed on the screen.")
        print("\nTrying to download the QR code image locally for you...")

        qr_url = f"https://api.green-api.com/waInstance{instance_id}/qr/{token}"
        try:
            q_res = requests.get(qr_url, timeout=15)
            q_data = q_res.json() if q_res.status_code == 200 else {}
            if q_data.get("type") == "qrCode" and q_data.get("message"):
                b64_data = q_data["message"]
                with open("qr_code.png", "wb") as f:
                    f.write(base64.b64decode(b64_data))
                print("✅ QR code saved locally as: qr_code.png")
                print("   Open 'qr_code.png' on your computer and scan it with WhatsApp!")
        except Exception as err:
            print(f"   Could not fetch QR code image directly: {err}")

        print("\nOnce you scan the QR code on your phone, re-run this script:")
        print("   python find_chat_id.py")
        return

    # Step 2: If authorized, retrieve all chats
    print("\nFetching connected chats, groups, and channels...")
    url = f"https://api.green-api.com/waInstance{instance_id}/getChats/{token}"

    try:
        res = requests.get(url, timeout=15)
        if res.status_code != 200:
            print(f"Error ({res.status_code}): {res.text}")
            return

        chats = res.json()
        if not chats:
            print("\nNo chats found yet in your active history.")
            print("💡 Tip: Send or open a message in your Channel or Group on your phone, then run this again!")
            return

        print("\n" + "=" * 65)
        print("   FOUND WHATSAPP CHATS / GROUPS / CHANNELS")
        print("=" * 65)

        for i, c in enumerate(chats, 1):
            chat_id = c.get("id", "")
            name = c.get("name") or "Unnamed"
            chat_type = c.get("type", "chat")

            if "@newsletter" in chat_id:
                category = "📢 CHANNEL"
            elif "@g.us" in chat_id:
                category = "👥 GROUP"
            elif "@c.us" in chat_id:
                category = "👤 CONTACT"
            else:
                category = f"💬 {chat_type.upper()}"

            print(f"\n{i}. [{category}] {name}")
            print(f"   Chat ID: {chat_id}")

        print("\n" + "=" * 65)
        print("👉 Copy the Chat ID above and set it in 'my_keys.txt':")
        print("   WHATSAPP_CHAT_ID=<your_chat_id>")
        print("   WHATSAPP_ENABLED=true")
        print("=" * 65)

    except Exception as e:
        print(f"Failed to fetch chats: {e}")


if __name__ == "__main__":
    main()
