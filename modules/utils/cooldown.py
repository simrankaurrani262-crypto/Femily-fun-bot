"""
Cooldown system for commands
"""
from datetime import datetime, timedelta
from database import db
import logging

logger = logging.getLogger(__name__)

class CooldownManager:
    """Manage command cooldowns"""
    
    @staticmethod
    def check_cooldown(user_id, command_name, cooldown_seconds):
        """Check if command is on cooldown"""
        user = db.get_user(user_id)
        if not user:
            return True, 0
        
        last_used_key = f'last_{command_name}'
        last_used = user.get(last_used_key)
        
        if not last_used:
            return True, 0
        
        elapsed = (datetime.utcnow() - last_used).total_seconds()
        remaining = cooldown_seconds - elapsed
        
        if remaining > 0:
            return False, remaining
        return True, 0
    
    @staticmethod
    def set_cooldown(user_id, command_name):
        """Set cooldown for command"""
        updates = {f'last_{command_name}': datetime.utcnow()}
        db.update_user(user_id, updates)
    
    @staticmethod
    def format_time(seconds):
        """Format seconds to readable time"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"