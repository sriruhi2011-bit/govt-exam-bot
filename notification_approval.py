# notification_approval.py
"""
Notification Approval & Broadcasting Manager.
Handles admin confirmation and public channel broadcast for official exam notifications.
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List

from config.settings import (
    DATA_DIR,
    CHANNEL_ID,
    KAN_CHANNEL_ID,
    WHATSAPP_CHAT_ID
)
from config.logger import setup_logger
from telegram_poster import TelegramPoster, run_async
from whatsapp_poster import WhatsAppPoster

logger = setup_logger("notif_approval")
REGISTRY_FILE = os.path.join(DATA_DIR, "notifications_registry.json")


class NotificationApprovalManager:
    def __init__(self):
        self.ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.poster = TelegramPoster()
        self.wa = WhatsAppPoster()
        self.admin_wa_chat = os.environ.get("ADMIN_WHATSAPP_ID", WHATSAPP_CHAT_ID)

    def get_ist_now(self):
        return datetime.now(self.ist_offset)

    def load_registry(self) -> Dict[str, Any]:
        if os.path.exists(REGISTRY_FILE):
            try:
                with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading notification registry: {e}")
        return {}

    def save_registry(self, data: Dict[str, Any]):
        try:
            with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving notification registry: {e}")

    # ════════════════════════════════════════════════════
    # APPROVE & BROADCAST TO PUBLIC GROUP / CHANNEL
    # ════════════════════════════════════════════════════
    def approve(self, notification_id: str = None) -> bool:
        """
        Approves an exam notification and immediately broadcasts the PDF
        and 1-line simple caption to the public Telegram channel & WhatsApp.
        """
        registry = self.load_registry()
        if not registry:
            print("❌ No notifications found in registry.")
            return False

        target_id = notification_id
        if not target_id:
            # Find latest pending_admin notification
            pending = [k for k, v in registry.items() if v.get("status") == "pending_admin"]
            if not pending:
                print("ℹ️ No pending exam notifications awaiting approval.")
                return False
            target_id = pending[-1]

        if target_id not in registry:
            print(f"❌ Notification ID '{target_id}' not found.")
            return False

        item = registry[target_id]
        if item.get("status") == "broadcasted":
            print(f"⚠️ Notification '{target_id}' has already been broadcasted.")
            return True

        pdf_path = item.get("pdf_path")
        caption = item.get("caption")
        agency = item.get("agency")
        title = item.get("title")

        # Cross-platform path resolution (e.g. Windows path on Linux runner)
        if pdf_path and not os.path.exists(pdf_path):
            filename = os.path.basename(pdf_path.replace("\\", "/"))
            candidate = os.path.join(DATA_DIR, "notifications", filename)
            if os.path.exists(candidate):
                pdf_path = candidate
                item["pdf_path"] = candidate

        if not pdf_path or not os.path.exists(pdf_path):
            url = item.get("url")
            if url:
                print(f"   Downloading PDF from {url}...")
                from exam_notification_monitor import ExamNotificationMonitor
                res = ExamNotificationMonitor().download_pdf(url, agency, title)
                if res:
                    pdf_path = res[0]
                    item["pdf_path"] = pdf_path
                    self.save_registry(registry)

        if not pdf_path or not os.path.exists(pdf_path):
            print(f"❌ PDF file not found and could not be downloaded for {target_id}")
            return False

        print("\n" + "=" * 65)
        print(f"   📢 BROADCASTING EXAM NOTIFICATION [{target_id}] TO GROUPS")
        print("=" * 65)
        print(f"   🏛️ Agency:  {agency}")
        print(f"   📄 Caption: {caption}")
        print(f"   📁 File:    {os.path.basename(pdf_path)}")

        tg_success = False
        wa_success = False

        # 1. Broadcast to Telegram Channel (@kansiri_daily_updates)
        try:
            print(f"   📤 Posting PDF to Telegram ({CHANNEL_ID})...")
            tg_html_caption = f"<b>{caption}</b>\n\n📌 <i>Official Notification Document</i>"
            tg_success = run_async(self.poster.send_document(
                file_path=pdf_path,
                caption=tg_html_caption,
                target_channel=CHANNEL_ID
            ))
            if tg_success:
                print("   ✅ Telegram broadcast successful!")
        except Exception as e:
            logger.error(f"Telegram broadcast error: {e}")
            print(f"   ⚠️ Telegram broadcast failed: {e}")

        # 2. Broadcast to WhatsApp Community / Channel (if enabled)
        if self.wa.is_enabled:
            try:
                print("   📤 Posting PDF to WhatsApp Community / Channel...")
                wa_md_caption = f"*{caption}*\n\n> Official Notification Document"
                wa_success = self.wa.send_document(
                    file_path=pdf_path,
                    caption=wa_md_caption
                )
                if wa_success:
                    print("   ✅ WhatsApp broadcast successful!")
            except Exception as e:
                logger.error(f"WhatsApp broadcast error: {e}")
                print(f"   ⚠️ WhatsApp broadcast failed: {e}")

        # Update registry state
        now_str = self.get_ist_now().strftime("%Y-%m-%d %H:%M:%S")
        item["status"] = "broadcasted"
        item["approved_at"] = now_str
        item["broadcasted_at"] = now_str
        registry[target_id] = item
        self.save_registry(registry)

        # Notify admin of completion
        confirm_text = f"✅ *NOTIFICATION BROADCASTED SUCCESSFULLY*\n\nID: `{target_id}`\nCaption: _{caption}_"
        if self.admin_wa_chat and self.wa.is_enabled:
            try:
                self.wa.send_text(confirm_text, target_chat=self.admin_wa_chat)
            except Exception:
                pass

        print(f"\n🎉 Notification [{target_id}] approved and published successfully!")
        return True

    # ════════════════════════════════════════════════════
    # REJECT NOTIFICATION
    # ════════════════════════════════════════════════════
    def reject(self, notification_id: str = None) -> bool:
        """Marks an exam notification as rejected so it is not broadcasted"""
        registry = self.load_registry()
        target_id = notification_id

        if not target_id:
            pending = [k for k, v in registry.items() if v.get("status") == "pending_admin"]
            if not pending:
                print("ℹ️ No pending exam notifications to reject.")
                return False
            target_id = pending[-1]

        if target_id not in registry:
            print(f"❌ Notification ID '{target_id}' not found.")
            return False

        registry[target_id]["status"] = "rejected"
        registry[target_id]["rejected_at"] = self.get_ist_now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_registry(registry)

        print(f"🚫 Notification [{target_id}] marked as REJECTED.")
        return True

    # ════════════════════════════════════════════════════
    # LIST NOTIFICATIONS
    # ════════════════════════════════════════════════════
    def list_notifications(self, status: str = None):
        """Displays formatted summary of all captured notifications"""
        registry = self.load_registry()
        if not registry:
            print("\nℹ️ No notifications captured yet. Run 'python main.py check-notifications' to scan.")
            return

        print("\n" + "=" * 75)
        print("   📋 OFFICIAL EXAM NOTIFICATIONS REGISTRY")
        print("=" * 75)
        for nid, item in registry.items():
            st = item.get("status", "unknown").upper()
            if status and item.get("status") != status:
                continue

            icon = "🟡" if st == "PENDING_ADMIN" else ("🟢" if st == "BROADCASTED" else "🔴")
            print(f"\n{icon} [{nid}] - {st}")
            print(f"   🏛️ Agency:   {item.get('agency')}")
            print(f"   📄 Title:    {item.get('title')}")
            print(f"   📝 Caption:  {item.get('caption')}")
            print(f"   📅 Detected: {item.get('detected_at')}")
            if item.get('broadcasted_at'):
                print(f"   🚀 Posted:   {item.get('broadcasted_at')}")
            print(f"   📁 PDF:      {os.path.basename(item.get('pdf_path', ''))}")
        print("\n" + "=" * 75)


if __name__ == "__main__":
    mgr = NotificationApprovalManager()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        arg = sys.argv[2] if len(sys.argv) > 2 else None
        if cmd == "approve":
            mgr.approve(arg)
        elif cmd == "reject":
            mgr.reject(arg)
        elif cmd in ["list", "status"]:
            mgr.list_notifications()
    else:
        mgr.list_notifications()
