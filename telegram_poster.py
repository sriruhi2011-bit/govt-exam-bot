# telegram_poster.py
"""
Professional Telegram Posting Engine for Aspirant Master Bot.
Supports:
- Sending rich HTML-formatted messages with tag-safety fallback
- Multi-question interactive Quiz Polls with explanations
- Dual-channel support (Primary English channel & Kannada channel)
- Automatic length-splitting and error handling
"""

import asyncio
import time
import requests
from telegram import Bot
from telegram.constants import ParseMode
from datetime import datetime
import html

from config.settings import BOT_TOKEN, CHANNEL_ID, KAN_BOT_TOKEN, KAN_CHANNEL_ID, TELEGRAM_MESSAGE_SPLIT_LENGTH, TELEGRAM_DELAY_SECONDS
from config.logger import setup_logger

logger = setup_logger("telegram")


class TelegramPoster:
    def __init__(self, bot_token: str = None, channel_id: str = None):
        self.token = bot_token or BOT_TOKEN
        self.channel = channel_id or CHANNEL_ID

    def _get_bot(self):
        return Bot(token=self.token)

    async def send_text(self, text: str, target_channel: str = None) -> bool:
        """Send formatted text message with HTML parsing and plain-text fallback"""
        chat_id = target_channel or self.channel
        try:
            if len(text) > TELEGRAM_MESSAGE_SPLIT_LENGTH:
                parts = []
                current = ""
                for line in text.split('\n'):
                    if len(current) + len(line) + 1 > TELEGRAM_MESSAGE_SPLIT_LENGTH:
                        parts.append(current)
                        current = line
                    else:
                        current += '\n' + line if current else line
                if current:
                    parts.append(current)

                for part in parts:
                    await self._send_single_message(chat_id, part)
                    await asyncio.sleep(1)
            else:
                await self._send_single_message(chat_id, text)

            return True
        except Exception as e:
            logger.error(f"Send text error: {e}")
            return False

    async def _send_single_message(self, chat_id: str, text: str):
        bot = self._get_bot()
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
        except Exception as html_err:
            logger.warning(f"HTML send failed ({html_err}), retrying without parse_mode...")
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                disable_web_page_preview=True
            )

    async def send_quiz(self, quiz_data: dict, target_channel: str = None) -> bool:
        """Send an interactive Telegram Quiz Poll with correct answer & explanation"""
        chat_id = target_channel or self.channel
        try:
            question = quiz_data['question'][:300]
            options = [opt[:100] for opt in quiz_data['options']][:10]
            correct_id = quiz_data.get('correct_option_id', 0)
            explanation = quiz_data.get('explanation', '')[:200]
            bot = self._get_bot()

            await bot.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                type='quiz',
                correct_option_id=correct_id,
                explanation=explanation,
                is_anonymous=True
            )
            await asyncio.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Send quiz poll error: {e}")
            return False

    async def send_poll_series(self, polls: list, target_channel: str = None) -> tuple:
        chat_id = target_channel or self.channel
        ok = 0
        fail = 0
        for i, p in enumerate(polls, 1):
            logger.info(f"   Posting quiz poll {i}/{len(polls)}...")
            res = await self.send_quiz(p, target_channel=chat_id)
            if res:
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(2)
        return ok, fail


def run_async(coro):
    """Run async coroutine synchronously"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

