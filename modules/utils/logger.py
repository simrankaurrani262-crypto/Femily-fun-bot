"""
Logging configuration
"""
import logging
import os
from config import LOG_LEVEL

def setup_logger(name):
    """Setup logger for module"""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # File handler
    fh = logging.FileHandler('logs/bot.log')
    fh.setLevel(LOG_LEVEL)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger