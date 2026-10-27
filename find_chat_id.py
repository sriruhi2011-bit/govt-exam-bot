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

    # Step 2: If authorized, retrieve chats and contacts
    print("\nFetching connected groups and contacts...")
    
    chats = []
    # Try getChats first
    try:
        url_chats = f"https://api.green-api.com/waInstance{instance_id}/getChats/{token}"
        c_res = requests.get(url_chats, timeout=15)
        if c_res.status_code == 200 and isinstance(c_res.json(), list):
            chats.extend(c_res.json())
    except:
        pass

    # Try getContacts
    try:
        url_contacts = f"https://api.green-api.com/waInstance{instance_id}/getContacts/{token}"
        k_res = requests.get(url_contacts, timeout=15)
        if k_res.status_code == 200 and isinstance(k_res.json(), list):
            for c in k_res.json():
                if c.get("id") and not any(x.get("id") == c.get("id") for x in chats):
                    chats.append(c)
    except:
        pass

    # Filter for groups and channels (and named chats)
    relevant = []
    for c in chats:
        cid = c.get("id", "")
        cname = c.get("name") or c.get("contactName") or ""
        if "@newsletter" in cid:
            relevant.append((1, "📢 CHANNEL", cname or "WhatsApp Channel", cid))
        elif "@g.us" in cid:
            relevant.append((2, "👥 GROUP", cname or "Unnamed Group", cid))

    if relevant:
        relevant.sort(key=lambda x: (x[0], x[2]))
        print("\n" + "=" * 65)
        print("   FOUND WHATSAPP GROUPS & CHANNELS")
        print("=" * 65)
        for i, (_, cat, name, cid) in enumerate(relevant, 1):
            print(f"\n{i}. [{cat}] {name}")
            print(f"   Chat ID: {cid}")

        print("\n" + "=" * 65)
        print("👉 Copy your target Chat ID and set it in 'my_keys.txt':")
        print("   WHATSAPP_CHAT_ID=<your_chat_id>")
        print("   WHATSAPP_ENABLED=true")
        print("=" * 65)
    else:
        print("\nNo groups or channels detected yet.")
        print("=" * 65)

    except Exception as e:
        print(f"Failed to fetch chats: {e}")


if __name__ == "__main__":
    main()
