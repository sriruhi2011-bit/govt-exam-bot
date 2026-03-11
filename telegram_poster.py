# telegram_poster.py
# WORKER 5 — Sends everything to Telegram channel

import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from datetime import datetime

from config.settings import BOT_TOKEN, CHANNEL_ID
from config.logger import setup_logger

logger = setup_logger("telegram")


class TelegramPoster:
    """
    Handles sending messages and quizzes to Telegram channel.
    
    What it can do:
    - Send text messages (news summaries)
    - Send quiz polls (interactive MCQs)
    - Split long messages automatically
    """
    
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.channel = CHANNEL_ID
    
    async def send_text(self, text):
        """Send a text message to the channel"""
        try:
            # Telegram has a 4096 character limit per message
            if len(text) > 4000:
                # Split into smaller parts
                parts = []
                current = ""
                for line in text.split('\n'):
                    if len(current) + len(line) + 1 > 4000:
                        parts.append(current)
                        current = line
                    else:
                        current += '\n' + line if current else line
                if current:
                    parts.append(current)
                
                for part in parts:
                    await self.bot.send_message(
                        chat_id=self.channel, text=part
                    )
                    await asyncio.sleep(2)
            else:
                await self.bot.send_message(
                    chat_id=self.channel, text=text
                )
            
            await asyncio.sleep(1)
            return True
            
        except Exception as e:
            logger.error(f"Send text error: {e}")
            return False
    
    async def send_quiz(self, quiz_data):
        """Send a quiz poll (interactive) to the channel"""
        try:
            question = quiz_data['question'][:300]
            options = quiz_data['options']
            
            await self.bot.send_poll(
                chat_id=self.channel,
                question=question,
                options=options,
                type='quiz',
                correct_option_id=quiz_data.get('correct_option_id', 0),
                explanation=quiz_data.get('explanation', '')[:200],
                is_anonymous=True
            )
            
            await asyncio.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"Send quiz error: {e}")
            return False
    
    async def post_news(self, posts):
        """Post all news messages"""
        logger.info(f"📤 Sending {len(posts)} news messages...")
        ok = 0
        fail = 0
        for i, post in enumerate(posts, 1):
            logger.info(f"   Sending {i}/{len(posts)}...")
            if await self.send_text(post):
                ok += 1
            else:
                fail += 1
        logger.info(f"   Done: {ok} sent, {fail} failed")
        return ok, fail
    
    async def post_quiz(self, quiz_posts):
        """Post all quiz items"""
        logger.info(f"📤 Sending {len(quiz_posts)} quiz items...")
        ok = 0
        fail = 0
        for i, (ptype, content) in enumerate(quiz_posts, 1):
            logger.info(f"   Sending {i}/{len(quiz_posts)}...")
            if ptype == "text":
                result = await self.send_text(content)
            elif ptype == "quiz":
                result = await self.send_quiz(content)
            else:
                continue
            if result:
                ok += 1
            else:
                fail += 1
        logger.info(f"   Done: {ok} sent, {fail} failed")
        return ok, fail


def run_async(coro):
    """Run async function from normal code"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# Test the bot when running this file directly
if __name__ == "__main__":
    print("Testing Telegram bot...")
    print("Sending a test message to your channel...")
    
    poster = TelegramPoster()
    result = run_async(
        poster.send_text("🧪 Test message — Bot is working! ✅")
    )
    
    if result:
        print("✅ SUCCESS! Check your Telegram channel!")
    else:
        print("❌ FAILED! Check your BOT_TOKEN and CHANNEL_ID in settings.py")