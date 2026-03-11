# config/logger.py
# DIARY — Records everything our program does

import logging
import os
from datetime import datetime

def setup_logger(name):
    """
    Creates a logger (diary writer) for a specific part of our program.
    
    What it does:
    - Writes messages to a file in the logs/ folder
    - Also shows messages on screen
    - Each day gets its own log file
    
    Parameters:
    - name: Who is writing (like "scraper" or "quiz_gen")
    """
    
    # Get the logs folder path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    # File handler — saves to a file
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"bot_{today}.log")
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Screen handler — shows on your screen
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(logging.INFO)
    
    # Format: What each log line looks like
    # Example: 2025-01-15 07:00:05 | scraper | INFO | Found 45 articles
    log_format = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(log_format)
    screen_handler.setFormatter(log_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(screen_handler)
    
    return logger