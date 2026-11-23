# approval_manager.py
"""
Daily Study Material Approval & Broadcast Workflow Manager.
Schedule:
- Before 5:30 PM IST (17:15 - 17:30): Generates both PDFs and sends to admin personally for confirmation.
- 5:30 PM - 6:00 PM IST: Admin review window (Reply 'APPROVE' / 'REJECT' or run 'python main.py approve').
- 6:35 PM IST (18:35): If approved, broadcasts both PDFs to the public group/channels.
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

from config.settings import (
    DATA_DIR,
    CHANNEL_ID,
    KAN_CHANNEL_ID,
    WHATSAPP_CHAT_ID,
    BOT_TOKEN,
    ADMIN_TELEGRAM_ID
)
from config.logger import setup_logger
from telegram_poster import TelegramPoster, run_async
from whatsapp_poster import WhatsAppPoster
from newspaper_pdf_pipeline import NewspaperPDFPipeline

logger = setup_logger("approval_manager")
APPROVAL_STATE_FILE = os.path.join(DATA_DIR, "pdf_approval_state.json")


class ApprovalManager:
    def __init__(self):
        self.ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.pipeline = NewspaperPDFPipeline()
        self.poster = TelegramPoster()
        self.wa = WhatsAppPoster()
        # Admin personal WhatsApp ID (e.g. 918660632301@c.us)
        self.admin_wa_chat = os.environ.get("ADMIN_WHATSAPP_ID", WHATSAPP_CHAT_ID)
        self.admin_tg_chat = os.environ.get("ADMIN_TELEGRAM_ID", ADMIN_TELEGRAM_ID)

    def get_ist_now(self):
        return datetime.now(self.ist_offset)

    def get_today_str(self):
        return self.get_ist_now().strftime("%Y-%m-%d")

    def load_state(self) -> Dict[str, Any]:
        if os.path.exists(APPROVAL_STATE_FILE):
            try:
                with open(APPROVAL_STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading approval state: {e}")
        return {}

    def save_state(self, state: Dict[str, Any]):
        try:
            with open(APPROVAL_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving approval state: {e}")

    # ════════════════════════════════════════════════════
    # STEP 1: GENERATE & SEND PERSONALLY (BEFORE 5:30 PM)
    # ════════════════════════════════════════════════════
    def prepare_and_send_for_approval(self, force_regenerate: bool = False) -> Dict[str, Any]:
        """
        Executed before 5:30 PM IST (e.g., 17:15 IST).
        Generates The Hindu and Prajavani PDFs and delivers them
        privately to the admin for review.
        """
        today = self.get_today_str()
        state = self.load_state()

        if today in state and not force_regenerate:
            if state[today].get("status") in ["approved", "posted"]:
                print(f"Today's PDFs already {state[today].get('status')}. Skipping.")
                return state[today]

        print("\n" + "=" * 60)
        print("   📰 STEP 1: GENERATING DAILY STUDY MATERIAL (THE HINDU & PRAJAVANI)")
        print("   ⏰ Target: Ready before 5:30 PM IST")
        print("=" * 60)

        # Generate both bilingual PDFs
        hindu_pdf, prajavani_pdf = self.pipeline.run_daily_generation()

        # Update state to pending_approval
        current_time_str = self.get_ist_now().strftime("%H:%M:%S")
        state[today] = {
            "the_hindu_pdf": hindu_pdf,
            "prajavani_pdf": prajavani_pdf,
            "status": "pending_approval",
            "generated_at": current_time_str,
            "approved_at": None,
            "posted_at": None
        }
        self.save_state(state)

        print("\n" + "=" * 60)
        print("   📤 SENDING TO ADMIN PERSONALLY FOR CONFIRMATION (BEFORE 6:00 PM)")
        print("=" * 60)

        approval_caption = (
            f"📑 *DAILY EXAM STUDY MATERIAL READY FOR REVIEW!*\n"
            f"📅 Date: {today}\n\n"
            f"1️⃣ *The Hindu* (Nordic Amber Focus — Bilingual)\n"
            f"2️⃣ *Prajavani* (KPSC Royal Crimson — Bilingual)\n\n"
            f"⏰ *Action Required before 6:00 PM IST:*\n"
            f"👉 Reply *APPROVE* (or run: `python main.py approve`) to confirm broadcast at 6:35 PM.\n"
            f"👉 Reply *REJECT* (or run: `python main.py reject`) to regenerate."
        )

        # 1. Send to WhatsApp Admin directly
        if self.wa.is_enabled and self.admin_wa_chat:
            try:
                print(f"   Delivering PDFs to Admin WhatsApp ({self.admin_wa_chat})...")
                self.wa.send_document(hindu_pdf, caption="📰 The Hindu (Bilingual Analysis)", target_chat=self.admin_wa_chat)
                self.wa.send_document(prajavani_pdf, caption="📰 Prajavani (Bilingual Analysis)", target_chat=self.admin_wa_chat)
                self.wa.send_text(approval_caption, target_chat=self.admin_wa_chat)
            except Exception as e:
                logger.warning(f"WhatsApp delivery error: {e}")

        # 2. Send to Telegram Admin if configured
        if self.admin_tg_chat:
            try:
                print(f"   Delivering PDFs to Admin Telegram ({self.admin_tg_chat})...")
                run_async(self.poster.send_document(hindu_pdf, caption="📰 <b>The Hindu — Daily Current Affairs & Analysis</b>", target_channel=self.admin_tg_chat))
                run_async(self.poster.send_document(prajavani_pdf, caption="📰 <b>Prajavani — Daily Analytical Digest</b>", target_channel=self.admin_tg_chat))
                run_async(self.poster.send_text(approval_caption, target_channel=self.admin_tg_chat))
            except Exception as e:
                logger.warning(f"Telegram delivery error: {e}")

        print("\n✅ PDFs delivered to admin personally. Awaiting approval before 6:00 PM IST.")
        return state[today]

    # ════════════════════════════════════════════════════
    # STEP 2: ADMIN CONFIRMATION (APPROVE / REJECT)
    # ════════════════════════════════════════════════════
    def approve(self) -> bool:
        """Confirm that PDFs are verified and ready for 6:35 PM public broadcast"""
        today = self.get_today_str()
        state = self.load_state()

        if today not in state:
            print("No generated PDFs found for today. Generating now...")
            self.prepare_and_send_for_approval()
            state = self.load_state()

        state[today]["status"] = "approved"
        state[today]["approved_at"] = self.get_ist_now().strftime("%H:%M:%S")
        self.save_state(state)

        confirmation_msg = (
            f"✅ *APPROVED!*\n"
            f"Today's *The Hindu* and *Prajavani* study material PDFs are confirmed.\n"
            f"They are scheduled to be posted to the group at *6:35 PM IST*."
        )
        print(f"\n{confirmation_msg}\n")

        if self.wa.is_enabled and self.admin_wa_chat:
            try:
                self.wa.send_text(confirmation_msg, target_chat=self.admin_wa_chat)
            except Exception as e:
                logger.warning(f"Failed to send confirmation to WhatsApp: {e}")

        return True

    def reject(self) -> bool:
        """Reject current PDFs and re-run generation pipeline"""
        today = self.get_today_str()
        print("\n❌ Rejecting current PDFs and re-generating fresh copy...")
        state = self.load_state()
        if today in state:
            state[today]["status"] = "rejected"
            self.save_state(state)

        # Re-run pipeline
        self.prepare_and_send_for_approval(force_regenerate=True)
        return True

    # ════════════════════════════════════════════════════
    # STEP 3: BROADCAST AT 6:35 PM IST (IF APPROVED)
    # ════════════════════════════════════════════════════
    def broadcast_at_635pm(self) -> bool:
        """
        Executed at 6:35 PM IST (18:35 IST).
        Checks approval status:
        - If 'approved': Posts both PDFs to Telegram channel and WhatsApp group.
        - If NOT approved: Aborts public posting and warns admin.
        """
        today = self.get_today_str()
        state = self.load_state()
        now_time = self.get_ist_now().strftime("%H:%M:%S")

        print("\n" + "=" * 60)
        print(f"   📢 6:35 PM BROADCAST DISPATCHER ({now_time} IST)")
        print("=" * 60)

        if today not in state:
            print("❌ No PDFs generated for today. Skipping public broadcast.")
            return False

        current_status = state[today].get("status")

        if current_status == "posted":
            print("✅ Already posted to public groups today.")
            return True

        if current_status != "approved":
            warning_msg = (
                f"⚠️ *BROADCAST BLOCKED AT 6:35 PM IST:*\n"
                f"The daily PDFs for {today} have status '{current_status}'.\n"
                f"They were NOT confirmed before 6:00 PM, so nothing was posted to the group.\n"
                f"To approve and send now, run: `python main.py approve` then `python main.py broadcast`."
            )
            print(f"\n{warning_msg}\n")
            if self.wa.is_enabled and self.admin_wa_chat:
                self.wa.send_text(warning_msg, target_chat=self.admin_wa_chat)
            return False

        # Status is APPROVED -> Proceed to public broadcast
        hindu_pdf = state[today].get("the_hindu_pdf")
        prajavani_pdf = state[today].get("prajavani_pdf")

        if not os.path.exists(hindu_pdf) or not os.path.exists(prajavani_pdf):
            print(f"❌ PDF file paths not found on disk: {hindu_pdf}, {prajavani_pdf}")
            return False

        print("   Posting 'The Hindu' study material to group...")
        hindu_caption = (
            f"📰 <b>The Hindu — Daily Current Affairs & Editorial Analysis</b>\n"
            f"📅 Date: {today}\n"
            f"🌐 Bilingual Edition: English & ಕನ್ನಡ"
        )
        run_async(self.poster.send_document(hindu_pdf, caption=hindu_caption, target_channel=CHANNEL_ID))
        if self.wa.is_enabled:
            self.wa.send_document(hindu_pdf, caption=self.wa.html_to_whatsapp(hindu_caption))

        print("   Posting 'Prajavani' study material to group...")
        prajavani_caption = (
            f"📰 <b>ಪ್ರಜಾವಾಣಿ — ದಿನಪತ್ರಿಕೆ ಸಮಗ್ರ ವಿಶ್ಲೇಷಣೆ</b>\n"
            f"📅 ದಿನಾಂಕ: {today}\n"
            f"🌐 Bilingual Edition: English & ಕನ್ನಡ"
        )
        target_kn = KAN_CHANNEL_ID if (KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID) else CHANNEL_ID
        run_async(self.poster.send_document(prajavani_pdf, caption=prajavani_caption, target_channel=target_kn))
        if self.wa.is_enabled:
            self.wa.send_document(prajavani_pdf, caption=self.wa.html_to_whatsapp(prajavani_caption))

        # Mark as posted
        state[today]["status"] = "posted"
        state[today]["posted_at"] = self.get_ist_now().strftime("%H:%M:%S")
        self.save_state(state)

        print("\n🎉 SUCCESS: Both daily study PDFs broadcasted to public group at 6:35 PM!")
        return True


if __name__ == "__main__":
    mgr = ApprovalManager()
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "prepare"
    if cmd in ["prepare", "generate", "prep"]:
        mgr.prepare_and_send_for_approval()
    elif cmd in ["approve", "confirm"]:
        mgr.approve()
    elif cmd in ["reject", "redo"]:
        mgr.reject()
    elif cmd in ["broadcast", "post"]:
        mgr.broadcast_at_635pm()
    else:
        print(f"Usage: python approval_manager.py [prepare|approve|reject|broadcast]")
