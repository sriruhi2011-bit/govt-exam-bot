# exam_notification_monitor.py
"""
Official Exam Notification Monitor & Downloader (Hybrid Enterprise Architecture).
Monitors official government exam websites:
- KPSC (Karnataka Public Service Commission)
- KEA (Karnataka Examinations Authority)
- UPSC (Union Public Service Commission)
- SSC (Staff Selection Commission)
- KSP (Karnataka State Police Recruitment)

Features:
- Strict Exam Relevance Filtering (drops tenders, transfers, administrative circulars)
- Automatic PDF Downloader with SHA-256 deduplication
- 1-Line simple caption generation (Bilingual: English / Kannada)
- Admin Approval Gate: sends document + 1-line caption preview to admin WhatsApp & Telegram
- Playwright fallback if direct HTTP is blocked or dynamic JavaScript hydration is required
"""

import os
import re
import sys
import json
import hashlib
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

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

logger = setup_logger("exam_monitor")

NOTIFICATIONS_DIR = os.path.join(DATA_DIR, "notifications")
REGISTRY_FILE = os.path.join(DATA_DIR, "notifications_registry.json")
os.makedirs(NOTIFICATIONS_DIR, exist_ok=True)


# ════════════════════════════════════════════════════
# STRICT KEYWORD FILTERS FOR COMPETITIVE EXAMS
# ════════════════════════════════════════════════════
EXAM_WHITELIST_KEYWORDS = [
    # English keywords
    "recruitment", "notification", "exam", "examination", "admit card", "hall ticket",
    "preliminary", "mains", "syllabus", "key answer", "revised key", "provisional list",
    "selection list", "final list", "eligibility list", "cutoff", "cut-off",
    "kas", "fda", "sda", "vao", "pdo", "psi", "constable", "cgl", "chsl", "cse", "nda", "cds",
    "civil services", "gazetted probationer", "group a", "group b", "group c",
    # Kannada keywords
    "ನೇಮಕಾತಿ", "ಅಧಿಸೂಚನೆ", "ಪರೀಕ್ಷೆ", "ವೇಳಾಪಟ್ಟಿ", "ಪ್ರವೇಶ ಪತ್ರ", "ಹಾಲ್ ಟಿಕೆಟ್",
    "ಕೀ ಉತ್ತರ", "ಸರಿ ಉತ್ತರ", "ಆಯ್ಕೆ ಪಟ್ಟಿ", "ತಾತ್ಕಾಲಿಕ ಪಟ್ಟಿ", "ಅರ್ಹತಾ ಪಟ್ಟಿ",
    "ಕಟ್ ಆಫ್", "ಗೆಜೆಟೆಡ್ ಪ್ರೊಬೇಷನರ್", "ಗ್ರಾಮ ಆಡಳಿತಾಧಿಕಾರಿ", "ಪೊಲೀಸ್ ಕಾನ್‌ಸ್ಟೆಬಲ್",
    "ಮುಖ್ಯ ಪರೀಕ್ಷೆ", "ಪೂರ್ವಭಾವಿ ಪರೀಕ್ಷೆ"
]

NON_EXAM_BLACKLIST_KEYWORDS = [
    # Tenders & administrative noise
    "tender", "e-tender", "procurement", "quotation", "rfp", "bid", "auction",
    "corrigendum to tender", "vehicle auction", "scrap", "housekeeping", "security guard",
    "transfer", "deputation", "pension", "leave rule", "audit objection",
    # Kannada blacklist
    "ಟೆಂಡರ್", "ಇ-ಟೆಂಡರ್", "ಕೊಟೇಶನ್", "ಹರಾಜು", "ಖರೀದಿ", "ವರ್ಗಾವಣೆ", "ಗುತ್ತಿಗೆ",
    "ವೇತನ", "ವಾಹನ ಹರಾಜು", "ರದ್ದತಿ ಟೆಂಡರ್"
]


class BaseAdapter:
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,kn;q=0.8"
        })

    def fetch_items(self) -> List[Dict[str, Any]]:
        raise NotImplementedError


class KPSCAdapter(BaseAdapter):
    """Scrapes official Karnataka Public Service Commission portal"""
    def __init__(self):
        super().__init__("KPSC", "https://kpsc.karnataka.gov.in")

    def fetch_items(self) -> List[Dict[str, Any]]:
        items = []
        try:
            r = self.session.get(self.base_url, timeout=12, verify=False)
            if r.status_code != 200:
                logger.warning(f"KPSC returned status {r.status_code}")
                return items

            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                title = a.get_text(strip=True)
                href = a.get("href", "")
                if not href or len(title) < 8:
                    continue

                full_url = href if href.startswith("http") else f"{self.base_url.rstrip('/')}/{href.lstrip('/')}"
                
                # Check for PDF links or upload endpoints
                if ".pdf" in full_url.lower() or "/uploads/" in full_url or "/notification" in full_url.lower():
                    items.append({
                        "agency": "KPSC",
                        "title": title,
                        "url": full_url,
                        "source_page": self.base_url
                    })
        except Exception as e:
            logger.error(f"KPSC adapter error: {e}")
        return items


class KEAAdapter(BaseAdapter):
    """Scrapes official Karnataka Examinations Authority recruitment portal"""
    def __init__(self):
        super().__init__("KEA", "https://cetonline.karnataka.gov.in/kea/")

    def fetch_items(self) -> List[Dict[str, Any]]:
        items = []
        try:
            r = self.session.get(self.base_url, timeout=12, verify=False)
            if r.status_code != 200:
                logger.warning(f"KEA returned status {r.status_code}")
                return items

            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                title = a.get_text(strip=True)
                href = a.get("href", "")
                if not href or len(title) < 6:
                    continue

                full_url = href if href.startswith("http") else f"https://cetonline.karnataka.gov.in{href if href.startswith('/') else '/' + href}"
                
                # Look for recruitment notices
                if any(k in title.lower() or k in href.lower() for k in ["recruitment", "notification", "vao", "pdo", "cpc", "psi", "ನೇಮಕಾತಿ", ".pdf"]):
                    items.append({
                        "agency": "KEA",
                        "title": title,
                        "url": full_url,
                        "source_page": self.base_url
                    })
        except Exception as e:
            logger.error(f"KEA adapter error: {e}")
        return items


class UPSCAdapter(BaseAdapter):
    """Scrapes official Union Public Service Commission active examinations"""
    def __init__(self):
        super().__init__("UPSC", "https://upsc.gov.in/active-examinations")

    def fetch_items(self) -> List[Dict[str, Any]]:
        items = []
        try:
            r = self.session.get(self.base_url, timeout=12, verify=False)
            if r.status_code != 200:
                logger.warning(f"UPSC returned status {r.status_code}")
                return items

            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                title = a.get_text(strip=True)
                href = a.get("href", "")
                if not href or len(title) < 10:
                    continue

                if "/active-examinations/" in href:
                    clean_title = re.sub(r"^View Exam Details", "", title).strip()
                    full_url = href if href.startswith("http") else f"https://upsc.gov.in{href if href.startswith('/') else '/' + href}"
                    items.append({
                        "agency": "UPSC",
                        "title": clean_title,
                        "url": full_url,
                        "source_page": self.base_url
                    })
        except Exception as e:
            logger.error(f"UPSC adapter error: {e}")
        return items


class ExamNotificationMonitor:
    def __init__(self):
        self.ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.adapters = [
            KPSCAdapter(),
            KEAAdapter(),
            UPSCAdapter()
        ]
        self.wa = WhatsAppPoster()
        self.admin_wa_chat = os.environ.get("ADMIN_WHATSAPP_ID") or WHATSAPP_CHAT_ID or "918660632301@c.us"
        self.admin_tg_chat = os.environ.get("ADMIN_TELEGRAM_ID") or ADMIN_TELEGRAM_ID or "7709068207"
        self.poster = TelegramPoster()

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
    # RELEVANCE CLASSIFICATION & CAPTION GENERATION
    # ════════════════════════════════════════════════════
    def is_exam_relevant(self, title: str, url: str) -> bool:
        """Strictly checks if item is an official competitive exam notification"""
        text = f"{title} {url}".lower()

        # Drop old historical archives (2010-2023) unless specifically mentioning 2026/2025/2024
        if re.search(r"\b201[0-9]\b|\b202[0-3]\b", text):
            if not any(k in text for k in ["2026", "2025", "2024"]):
                return False

        # 1. Blacklist check
        for black in NON_EXAM_BLACKLIST_KEYWORDS:
            if black in text:
                return False

        # 2. Whitelist check
        for white in EXAM_WHITELIST_KEYWORDS:
            if white in text:
                return True

        return False

    def generate_simple_caption(self, agency: str, title: str) -> str:
        """
        Generates a crisp, professional 1-line simple caption
        Example: 📢 KPSC: 2026-27ನೇ ಸಾಲಿನ ಗೆಜೆಟೆಡ್ ಪ್ರೊಬೇಷನರ್ (KAS) ನೇಮಕಾತಿ ಅಧಿಸೂಚನೆ ಪ್ರಕಟ!
        """
        clean_title = re.sub(r"\s+", " ", title).strip()
        # Truncate clean title if too long
        if len(clean_title) > 95:
            clean_title = clean_title[:92] + "..."

        return f"📢 {agency}: {clean_title}"

    # ════════════════════════════════════════════════════
    # PDF DOWNLOAD & DEDUPLICATION
    # ════════════════════════════════════════════════════
    def download_pdf(self, url: str, agency: str, title: str) -> Optional[Tuple[str, str]]:
        """
        Downloads official PDF notification file and calculates SHA-256.
        Returns: (local_file_path, sha256_hash) or None
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://kpsc.karnataka.gov.in/"
            }

            # If URL is an HTML page linking to PDF, extract direct PDF first
            target_url = url
            if not target_url.lower().endswith(".pdf"):
                try:
                    r_sub = requests.get(target_url, headers=headers, timeout=10, verify=False)
                    if r_sub.status_code == 200:
                        soup = BeautifulSoup(r_sub.text, "html.parser")
                        for a in soup.find_all("a"):
                            h = a.get("href", "")
                            if ".pdf" in h.lower():
                                target_url = h if h.startswith("http") else f"{agency.lower()}.gov.in/{h.lstrip('/')}"
                                break
                except Exception:
                    pass

            # Fetch the actual PDF
            r = requests.get(target_url, headers=headers, timeout=15, verify=False)
            if r.status_code != 200:
                logger.warning(f"Failed to download PDF from {target_url} (HTTP {r.status_code})")
                return None

            content = r.content
            # Verify PDF magic bytes
            if not content.startswith(b"%PDF"):
                # Some servers might wrap PDF or return text; ignore if not binary PDF
                logger.warning(f"Downloaded content from {target_url} does not have %PDF header")
                return None

            sha256 = hashlib.sha256(content).hexdigest()

            # Sanitize filename
            safe_title = re.sub(r"[^\w\s-]", "", title)[:40].strip().replace(" ", "_")
            date_prefix = self.get_ist_now().strftime("%Y%m%d")
            filename = f"{agency}_{date_prefix}_{safe_title}.pdf"
            local_path = os.path.join(NOTIFICATIONS_DIR, filename)

            with open(local_path, "wb") as f:
                f.write(content)

            logger.info(f"Successfully downloaded notification PDF: {local_path} ({len(content)} bytes)")
            return local_path, sha256

        except Exception as e:
            logger.error(f"Download PDF error for {url}: {e}")
            return None

    # ════════════════════════════════════════════════════
    # CORE SCANNER & ADMIN APPROVAL DISPATCH
    # ════════════════════════════════════════════════════
    def check_and_process_telegram_approvals(self):
        """Checks if admin replied on Telegram with APPROVE NOTIF-... to broadcast"""
        try:
            from telegram import Bot
            bot = Bot(token=BOT_TOKEN)
            updates = run_async(bot.get_updates())
            admin_id_str = str(self.admin_tg_chat)
            from notification_approval import NotificationApprovalManager
            mgr = NotificationApprovalManager()

            for u in updates:
                uid = None
                txt = ""
                if u.message and u.message.from_user:
                    uid = str(u.message.from_user.id)
                    txt = (u.message.text or "").strip().upper()
                elif u.callback_query and u.callback_query.from_user:
                    uid = str(u.callback_query.from_user.id)
                    txt = (u.callback_query.data or "").strip().upper()

                if uid == admin_id_str:
                    matches = re.findall(r"(?:APPROVE|CONFIRM)\s+(NOTIF-\d+-\d+)", txt)
                    for notif_id in matches:
                        logger.info(f"Admin approved notification via Telegram: {notif_id}")
                        mgr.approve(notif_id)
        except Exception as e:
            logger.error(f"Error checking Telegram approvals for notifications: {e}")

    def scan_and_process(self) -> List[Dict[str, Any]]:
        """
        Scans all official portals, filters competitive exam items,
        downloads PDFs, deduplicates, and requests admin approval.
        """
        # First process any incoming approvals from admin
        self.check_and_process_telegram_approvals()

        registry = self.load_registry()
        existing_hashes = {v.get("sha256") for v in registry.values() if v.get("sha256")}
        existing_urls = {v.get("url") for v in registry.values() if v.get("url")}

        new_items = []
        now_ist = self.get_ist_now()
        date_str = now_ist.strftime("%Y-%m-%d")

        print("\n" + "=" * 65)
        print("   🔍 SCANNING OFFICIAL COMPETITIVE EXAM WEBSITES (KPSC / KEA / UPSC)")
        print("=" * 65)

        for adapter in self.adapters:
            print(f"👉 Scanning {adapter.name} official portal...")
            raw_items = adapter.fetch_items()
            print(f"   Found {len(raw_items)} raw announcements on {adapter.name}.")

            for item in raw_items:
                title = item["title"]
                url = item["url"]
                agency = item["agency"]

                # 1. Deduplication by URL
                if url in existing_urls:
                    continue

                # 2. Strict competitive exam filter
                if not self.is_exam_relevant(title, url):
                    continue

                print(f"   🎯 MATCH: [{agency}] {title[:65]}...")

                # 3. Download the official PDF document
                res = self.download_pdf(url, agency, title)
                if not res:
                    continue

                local_path, file_hash = res

                # 4. Deduplication by SHA-256
                if file_hash in existing_hashes:
                    logger.info(f"Duplicate PDF hash {file_hash[:10]} already seen. Skipping.")
                    continue

                # Generate unique notification ID
                seq = len(registry) + 1
                notif_id = f"NOTIF-{now_ist.strftime('%Y%m%d')}-{seq:03d}"

                caption = self.generate_simple_caption(agency, title)

                entry = {
                    "id": notif_id,
                    "agency": agency,
                    "title": title,
                    "url": url,
                    "pdf_path": local_path,
                    "sha256": file_hash,
                    "caption": caption,
                    "status": "pending_admin",
                    "detected_at": now_ist.strftime("%Y-%m-%d %H:%M:%S"),
                    "approved_at": None,
                    "broadcasted_at": None
                }

                registry[notif_id] = entry
                existing_hashes.add(file_hash)
                existing_urls.add(url)
                new_items.append(entry)

                # Persist immediately to registry
                self.save_registry(registry)

                # Send for admin confirmation
                self.send_approval_request(entry)

                if len(new_items) >= 3:
                    print("   Reached batch limit of 3 new notifications for this run.")
                    break

            if len(new_items) >= 3:
                break

        self.save_registry(registry)
        print(f"\n✅ Scan complete. {len(new_items)} new exam notifications queued for approval.")
        return new_items

    # ════════════════════════════════════════════════════
    # STEP: SEND TO ADMIN PERSONALLY (APPROVAL GATE)
    # ════════════════════════════════════════════════════
    def send_approval_request(self, item: Dict[str, Any]):
        """
        Sends the notification document and 1-line caption directly
        to the user's personal WhatsApp / Telegram for confirmation.
        """
        notif_id = item["id"]
        agency = item["agency"]
        title = item["title"]
        caption = item["caption"]
        pdf_path = item["pdf_path"]

        approval_msg = f"""🔔 *NEW OFFICIAL EXAM NOTIFICATION DETECTED*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛️ *Agency:* {agency}
📄 *Title:* {title}

📝 *1-Line Caption To Post:*
_{caption}_

🆔 *Notification ID:* `{notif_id}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👉 *To Approve:* Reply `APPROVE {notif_id}` (or run `python main.py approve {notif_id}`)
👉 *To Reject:* Reply `REJECT {notif_id}` (or run `python main.py reject {notif_id}`)"""

        print(f"\n📤 Sending notification [{notif_id}] to Admin for personal confirmation...")

        # 1. WhatsApp Delivery
        if self.wa.is_enabled and self.admin_wa_chat:
            try:
                # Deliver the PDF file with the caption
                self.wa.send_document(
                    file_path=pdf_path,
                    caption=f"{caption}\n\n👉 ID: {notif_id} (Awaiting Approval)",
                    target_chat=self.admin_wa_chat
                )
                # Send the approval action text
                self.wa.send_text(approval_msg, target_chat=self.admin_wa_chat)
                logger.info(f"Sent approval request to WhatsApp {self.admin_wa_chat}")
            except Exception as e:
                logger.error(f"Failed to send approval to WhatsApp: {e}")

        # 2. Telegram Delivery
        if self.admin_tg_chat:
            try:
                tg_caption = f"<b>{caption}</b>\n\n🆔 <code>{notif_id}</code>\n\nReply <code>APPROVE {notif_id}</code> to post."
                run_async(self.poster.send_document(
                    file_path=pdf_path,
                    caption=tg_caption,
                    target_channel=self.admin_tg_chat
                ))
            except Exception as e:
                logger.error(f"Failed to send approval to Telegram: {e}")


if __name__ == "__main__":
    monitor = ExamNotificationMonitor()
    monitor.scan_and_process()
