# whatsapp_poster.py
"""
WhatsApp Poster for Aspirant Master Bot (Option 1: Green API Gateway).
Supports broadcasting to:
- WhatsApp Channels (Newsletters: 120363xxx@newsletter)
- WhatsApp Groups (120363xxx@g.us)
- Individual WhatsApp Chats (phone@c.us)

Features:
- Automatic conversion from Telegram HTML (<b>, <i>, <blockquote>) to WhatsApp Markdown (*bold*, _italic_, > quote)
- Formats Prelims MCQs with clean spoiler/quote answers suitable for WhatsApp Channels
- Fails gracefully if WhatsApp credentials are not yet configured (zero impact on Telegram)
"""

import re
import html
import requests
from typing import Dict, Any, List

from config.settings import (
    WHATSAPP_ENABLED,
    WHATSAPP_INSTANCE_ID,
    WHATSAPP_API_TOKEN,
    WHATSAPP_CHAT_ID
)
from config.logger import setup_logger

logger = setup_logger("whatsapp")


class WhatsAppPoster:
    def __init__(self, instance_id: str = None, api_token: str = None, chat_id: str = None):
        self.instance_id = instance_id or WHATSAPP_INSTANCE_ID
        self.api_token = api_token or WHATSAPP_API_TOKEN
        self.chat_id = chat_id or WHATSAPP_CHAT_ID
        self.is_enabled = bool(
            WHATSAPP_ENABLED and self.instance_id and self.api_token and self.chat_id
        )

    def html_to_whatsapp(self, text: str) -> str:
        """
        Converts Telegram HTML formatting to WhatsApp Markdown:
        - <b>, <strong> -> *bold*
        - <i>, <em> -> _italic_
        - <code> -> ```code```
        - <blockquote> -> > quoted lines
        - <u> -> preserved as clean text
        """
        if not text:
            return ""

        # Unescape basic HTML entities first
        out = text

        # Convert blockquotes: add '> ' to each line inside blockquote
        def blockquote_repl(match):
            content = match.group(1).strip()
            lines = content.split('\n')
            quoted = '\n'.join([f"> {line}" for line in lines])
            return f"\n{quoted}\n"

        out = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', blockquote_repl, out, flags=re.DOTALL | re.IGNORECASE)

        # Bold
        out = re.sub(r'<(?:b|strong)>(.*?)</(?:b|strong)>', r'*\1*', out, flags=re.DOTALL | re.IGNORECASE)

        # Italic
        out = re.sub(r'<(?:i|em)>(.*?)</(?:i|em)>', r'_\1_', out, flags=re.DOTALL | re.IGNORECASE)

        # Code
        out = re.sub(r'<code>(.*?)</code>', r'```\1```', out, flags=re.DOTALL | re.IGNORECASE)

        # Underline (WhatsApp doesn't have native underline, strip tag)
        out = re.sub(r'<u>(.*?)</u>', r'\1', out, flags=re.DOTALL | re.IGNORECASE)

        # Strip remaining HTML tags
        out = re.sub(r'<[^>]+>', '', out)

        # Decode HTML entities like &amp;, &lt;, &gt;
        out = html.unescape(out)

        # Clean multiple blank lines
        out = re.sub(r'\n{3,}', '\n\n', out)

        return out.strip()

    def send_text(self, text: str, target_chat: str = None) -> bool:
        """Send formatted text message to WhatsApp Channel or Group"""
        if not self.is_enabled:
            logger.debug("WhatsApp is not configured/enabled. Skipping.")
            return False

        chat_id = target_chat or self.chat_id
        wa_text = self.html_to_whatsapp(text)

        url = f"https://api.green-api.com/waInstance{self.instance_id}/sendMessage/{self.api_token}"
        payload = {
            "chatId": chat_id,
            "message": wa_text
        }

        try:
            logger.info(f"📤 Sending message to WhatsApp ({chat_id[:15]}...)...")
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                logger.info("   WhatsApp message sent successfully!")
                return True
            else:
                logger.error(f"   WhatsApp error {res.status_code}: {res.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"   WhatsApp send exception: {e}")
            return False

    def send_quiz_poll(self, quiz_data: Dict[str, Any], target_chat: str = None) -> bool:
        """
        Formats and sends an MCQ quiz question for WhatsApp Channels:
        Shows Question + Options A/B/C/D, with the answer in a WhatsApp quote.
        """
        if not self.is_enabled:
            return False

        question = quiz_data.get('question', '')
        options = quiz_data.get('options', [])
        correct_id = quiz_data.get('correct_option_id', 0)
        explanation = quiz_data.get('explanation', '')

        opts_text = "\n".join([f"*{chr(65 + i)}.* {opt}" for i, opt in enumerate(options)])
        correct_letter = chr(65 + correct_id) if 0 <= correct_id < len(options) else 'A'
        correct_text = options[correct_id] if 0 <= correct_id < len(options) else ''

        wa_post = f"""🧠 *PRELIMS MCQ PRACTICE*
━━━━━━━━━━━━━━━━━━━━━━━━━━
{question}

{opts_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━
> ✅ *Correct Answer: {correct_letter}* ({correct_text})
> 💡 *Explanation:* {explanation}
━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return self.send_text(wa_post, target_chat=target_chat)


if __name__ == "__main__":
    wp = WhatsAppPoster()
    sample_html = "<b>Good morning, future officers!</b>\n<blockquote>Article 200 & 201 details</blockquote>"
    print("WhatsApp Markdown conversion test:")
    print(wp.html_to_whatsapp(sample_html))
