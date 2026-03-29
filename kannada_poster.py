# kannada_poster.py
# WORKER 6 — Sends messages to Kannada Telegram channel

import asyncio
import requests
from telegram import Bot
from telegram.constants import ParseMode

from config.settings import KAN_BOT_TOKEN, KAN_CHANNEL_ID, TELEGRAM_MESSAGE_SPLIT_LENGTH, TELEGRAM_DELAY_SECONDS
from config.logger import setup_logger

logger = setup_logger("kan_poster")


class KannadaPoster:
    """
    Handles sending messages and quizzes to Kannada Telegram channel.
    
    What it can do:
    - Send text messages (news summaries in Kannada)
    - Send photos with captions
    - Send quiz polls (interactive MCQs in Kannada)
    - Split long messages automatically
    """
    
    def __init__(self):
        self.bot = Bot(token=KAN_BOT_TOKEN)
        self.channel = KAN_CHANNEL_ID
    
    async def send_text(self, text):
        """Send a text message to the Kannada channel"""
        try:
            if len(text) > TELEGRAM_MESSAGE_SPLIT_LENGTH:
                # Split into smaller parts
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
                    await self.bot.send_message(
                        chat_id=self.channel, text=part, parse_mode=ParseMode.HTML
                    )
                    await asyncio.sleep(TELEGRAM_DELAY_SECONDS * 2)
            else:
                await self.bot.send_message(
                    chat_id=self.channel, text=text, parse_mode=ParseMode.HTML
                )
            
            await asyncio.sleep(TELEGRAM_DELAY_SECONDS * 2)
            return True
            
        except Exception as e:
            logger.error(f"Send text error: {e}")
            return False
    
    async def send_photo_with_caption(self, photo_url, caption):
        """Send a photo with caption to the Kannada channel"""
        try:
            if not photo_url:
                return await self.send_text(caption)
            
            try:
                await self.bot.send_photo(
                    chat_id=self.channel,
                    photo=photo_url,
                    caption=caption[:1024],
                    parse_mode=ParseMode.HTML
                )
                await asyncio.sleep(TELEGRAM_DELAY_SECONDS * 2)
                return True
            except Exception as url_error:
                logger.warning(f"Could not send photo by URL: {url_error}")
            
            try:
                response = requests.get(photo_url, timeout=30)
                if response.status_code == 200:
                    await self.bot.send_photo(
                        chat_id=self.channel,
                        photo=response.content,
                        caption=caption[:1024],
                        parse_mode=ParseMode.HTML
                    )
                    await asyncio.sleep(TELEGRAM_DELAY_SECONDS * 2)
                    return True
            except Exception as e:
                logger.warning(f"Could not download image: {e}")
            
            return await self.send_text(caption)
            
        except Exception as e:
            logger.error(f"Send photo error: {e}")
            return await self.send_text(caption)
    
    async def send_quiz(self, quiz_data):
        """Send a quiz poll (interactive) to the Kannada channel"""
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
        """Post all news messages to Kannada channel"""
        logger.info(f"📤 Sending {len(posts)} Kannada news messages...")
        ok = 0
        fail = 0
        for i, post in enumerate(posts, 1):
            logger.info(f"   Sending {i}/{len(posts)}...")
            
            if isinstance(post, dict):
                text = post.get('text', '')
                image_url = post.get('image_url')
                if image_url:
                    result = await self.send_photo_with_caption(image_url, text)
                else:
                    result = await self.send_text(text)
            else:
                result = await self.send_text(post)
            
            if result:
                ok += 1
            else:
                fail += 1
        logger.info(f"   Done: {ok} sent, {fail} failed")
        return ok, fail
    
    async def post_quiz(self, quiz_posts):
        """Post all quiz items to Kannada channel"""
        logger.info(f"📤 Sending {len(quiz_posts)} Kannada quiz items...")
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
    print("Testing Kannada bot...")
    print("Sending a test message to your Kannada channel...")
    
    poster = KannadaPoster()
    result = run_async(
        poster.send_text("🧪 ಪರೀಕ್ಷಾ ಸಂದೇಶ - ಬಾಟ್ ಕೆಲಸ ಮಾಡುತ್ತಿದೆ! ✅")
    )
    
    if result:
        print("✅ SUCCESS! Check your Kannada Telegram channel!")
    else:
        print("❌ FAILED! Check your KAN_BOT_TOKEN and KAN_CHANNEL_ID in settings.py")