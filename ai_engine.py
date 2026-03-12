# ai_engine.py

import requests
import json
import time
from config.settings import (
    GEMINI_API_KEY, GROQ_API_KEY,
    CEREBRAS_API_KEY, OPENROUTER_API_KEY,
    AI_TIMEOUT_SECONDS
)
from config.logger import setup_logger

logger = setup_logger("ai_engine")


class AIEngine:

    def __init__(self):
        from config.settings import (
            GEMINI_API_KEY, GROQ_API_KEY,
            CEREBRAS_API_KEY, OPENROUTER_API_KEY
        )

        self.providers = []

        if GEMINI_API_KEY and "PASTE_" not in GEMINI_API_KEY and "YOUR_" not in GEMINI_API_KEY and len(GEMINI_API_KEY) > 10:
            self.providers.append({
                "name": "Gemini",
                "type": "gemini",
                "key": GEMINI_API_KEY,
                "model": "gemini-2.0-flash-lite",
                "url": "https://generativelanguage.googleapis.com/v1beta/models/",
                "rpm": 15,
                "fails": 0
            })
            logger.info(f"  Provider added: Google Gemini")

        if GROQ_API_KEY and "PASTE_" not in GROQ_API_KEY and "YOUR_" not in GROQ_API_KEY and len(GROQ_API_KEY) > 10:
            self.providers.append({
                "name": "Groq",
                "type": "openai_compatible",
                "key": GROQ_API_KEY,
                "model": "llama-3.1-8b-instant",
                "url": "https://api.groq.com/openai/v1/chat/completions",
                "rpm": 30,
                "fails": 0
            })
            logger.info(f"  Provider added: Groq")

        if CEREBRAS_API_KEY and "PASTE_" not in CEREBRAS_API_KEY and "YOUR_" not in CEREBRAS_API_KEY and len(CEREBRAS_API_KEY) > 10:
            self.providers.append({
                "name": "Cerebras",
                "type": "openai_compatible",
                "key": CEREBRAS_API_KEY,
                "model": "llama3.1-8b",
                "url": "https://api.cerebras.ai/v1/chat/completions",
                "rpm": 30,
                "fails": 0
            })
            logger.info(f"  Provider added: Cerebras")

        if OPENROUTER_API_KEY and "PASTE_" not in OPENROUTER_API_KEY and "YOUR_" not in OPENROUTER_API_KEY and len(OPENROUTER_API_KEY) > 10:
            self.providers.append({
                "name": "OpenRouter",
                "type": "openai_compatible",
                "key": OPENROUTER_API_KEY,
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "rpm": 20,
                "fails": 0
            })
            logger.info(f"  Provider added: OpenRouter")

        if not self.providers:
            raise ValueError("No AI providers! Add API keys in config/settings.py")

        self.current_provider_index = 0
        self.last_request_time = 0
        logger.info(f"AI Engine ready with {len(self.providers)} providers")

    def _get_provider(self):
        return self.providers[self.current_provider_index]

    def _switch_provider(self):
        old = self.providers[self.current_provider_index]["name"]
        self.current_provider_index = (self.current_provider_index + 1) % len(self.providers)
        new = self.providers[self.current_provider_index]["name"]
        logger.info(f"  Switching: {old} -> {new}")

    def _smart_delay(self):
        provider = self._get_provider()
        rpm = provider.get("rpm", 15)
        min_delay = 60.0 / rpm + 0.5
        elapsed = time.time() - self.last_request_time
        if elapsed < min_delay:
            time.sleep(min_delay - elapsed)
        self.last_request_time = time.time()

    def _call_gemini(self, provider, prompt, temperature, max_tokens):
        url = provider["url"] + provider["model"] + ":generateContent?key=" + provider["key"]
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}
        }
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=AI_TIMEOUT_SECONDS)
        if response.status_code == 200:
            result = response.json()
            try:
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()
            except (KeyError, IndexError):
                return None
        elif response.status_code == 429:
            return "RATE_LIMITED"
        else:
            logger.error(f"  Gemini error {response.status_code}")
            return None

    def _call_openai_compatible(self, provider, prompt, temperature, max_tokens):
        headers = {"Authorization": "Bearer " + provider["key"], "Content-Type": "application/json"}
        if provider["name"] == "OpenRouter":
            headers["HTTP-Referer"] = "https://github.com/newsbot"
        payload = {
            "model": provider["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = requests.post(provider["url"], headers=headers, json=payload, timeout=AI_TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        elif response.status_code == 429:
            return "RATE_LIMITED"
        else:
            logger.error(f"  {provider['name']} error {response.status_code}")
            return None

    def query(self, prompt, temperature=0.2, max_tokens=500):
        attempts = 0
        max_attempts = len(self.providers) * 3
        while attempts < max_attempts:
            provider = self._get_provider()
            attempts += 1
            self._smart_delay()
            try:
                if provider["type"] == "gemini":
                    result = self._call_gemini(provider, prompt, temperature, max_tokens)
                else:
                    result = self._call_openai_compatible(provider, prompt, temperature, max_tokens)
                if result == "RATE_LIMITED":
                    provider["fails"] += 1
                    if len(self.providers) > 1:
                        self._switch_provider()
                    else:
                        time.sleep(30)
                    continue
                elif result is not None:
                    provider["fails"] = 0
                    return result
                else:
                    provider["fails"] += 1
                    if provider["fails"] >= 3 and len(self.providers) > 1:
                        self._switch_provider()
                    else:
                        time.sleep(5)
            except requests.exceptions.Timeout:
                if len(self.providers) > 1:
                    self._switch_provider()
                else:
                    time.sleep(10)
            except Exception as e:
                logger.error(f"  Error: {str(e)}")
                time.sleep(5)
        return None

    def extract_json(self, text):
        if text is None:
            return None
        try:
            return json.loads(text)
        except Exception:
            pass
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except Exception:
            pass
        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except Exception:
            pass
        return None


def get_ai_engine():
    """Lazy initialization of AI engine"""
    global _ai_instance
    if _ai_instance is None:
        _ai_instance = AIEngine()
    return _ai_instance


# Lazy-loaded singleton instance
_ai_instance = None

# Backwards compatibility - ai = get_ai_engine()
# Removed auto-initialization at import time to prevent failures when no API keys are configured
