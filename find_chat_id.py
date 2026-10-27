# find_chat_id.py
"""
Helper script to list all WhatsApp chats, groups, and channels connected
to your Green API instance, along with their exact Chat IDs.
"""

import os
import requests

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

    print(f"\nConnecting to Green API Instance: {instance_id}...")
    url = f"https://api.green-api.com/waInstance{instance_id}/getChats/{token}"

    try:
        res = requests.get(url, timeout=15)
        if res.status_code != 200:
            print(f"Error ({res.status_code}): {res.text}")
            return

        chats = res.json()
        if not chats:
            print("No active chats found on this WhatsApp account.")
            return

        print("\n" + "=" * 65)
        print("   FOUND WHATSAPP CHATS / GROUPS / CHANNELS")
        print("=" * 65)

        for i, c in enumerate(chats, 1):
            chat_id = c.get("id", "")
            name = c.get("name") or "Unnamed"
            chat_type = c.get("type", "chat")

            # Determine category label
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
        print("👉 Copy the Chat ID of your target Channel/Group and set it as:")
        print("   WHATSAPP_CHAT_ID=<your_chat_id>")
        print("=" * 65)

    except Exception as e:
        print(f"Failed to fetch chats: {e}")

if __name__ == "__main__":
    main()
