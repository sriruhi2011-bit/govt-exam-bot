# ai_engine.py
# THE BRAIN — Talks to AI (Groq) for smart analysis

import requests
import json
import time
from config.settings import GROQ_API_KEY, GROQ_MODEL
from config.logger import setup_logger

logger = setup_logger("ai_engine")


class AIEngine:
    """
    This class handles ALL communication with the AI.
    
    How it works:
    1. We send a question/prompt (text) to Groq's servers
    2. Groq's AI (Llama 3.1) reads it and generates an answer
    3. We receive the answer back
    4. We extract useful information from the answer
    
    It's like texting a very smart friend who replies instantly.
    """
    
    def __init__(self):
        """Set up the AI engine"""
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.max_retries = 3  # Try 3 times if something fails
        logger.info("AI Engine ready (using Groq)")
    
    def query(self, prompt, temperature=0.2, max_tokens=500):
        """
        Send a question to AI and get the answer.
        
        Parameters:
        - prompt: The question/instruction we're sending
        - temperature: How creative the AI should be 
                      (0.0 = very focused, 1.0 = very creative)
        - max_tokens: Maximum length of AI's response
        
        Returns: The AI's response as text, or None if it failed
        """
        
        for attempt in range(self.max_retries):
            try:
                # Send request to Groq
                response = requests.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    },
                    timeout=60
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    answer = result['choices'][0]['message']['content']
                    return answer.strip()
                
                elif response.status_code == 429:
                    # Rate limited — too many requests, wait and retry
                    logger.warning(
                        f"Rate limited by Groq. Waiting 10 seconds..."
                    )
                    time.sleep(10)
                    continue
                
                else:
                    logger.error(
                        f"Groq API error {response.status_code}: "
                        f"{response.text[:200]}"
                    )
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Request timed out (attempt {attempt + 1})")
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"AI query error (attempt {attempt + 1}): {e}")
                time.sleep(5)
        
        logger.error("All AI query attempts failed!")
        return None
    
    def extract_json(self, text):
        """
        Extract JSON data from AI's response.
        
        Why? Sometimes AI returns JSON wrapped in extra text.
        This function finds and extracts just the JSON part.
        
        Example AI response:
        "Here is the analysis: {"is_relevant": true, "category": "Economy"}"
        This function extracts: {"is_relevant": true, "category": "Economy"}
        """
        
        if text is None:
            return None
        
        # Try 1: Maybe the whole text is valid JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try 2: Find JSON object {...} in the text
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Try 3: Find JSON array [...] in the text
        try:
            start = text.find('[')
            end = text.rfind(']') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        logger.error(f"Could not extract JSON from: {text[:200]}")
        return None


# Create ONE global AI engine that everyone uses
ai = AIEngine()