"""
/parents and /children commands
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def parents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View parents"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    if not family.get('parents'):
        await update.message.reply_text("❌ You have no parents registered")
        return
    
    parents_text = "<b>👪 YOUR PARENTS</b>\n\n"
    for parent_id in family['parents']:
        parent = db.get_user(parent_id)
        if parent:
            parents_text += f"• @{parent['username']} (Level {parent['level']})\n"
    
    await update.message.reply_text(parents_text, parse_mode="HTML")

async def children_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View children"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    if not family.get('children'):
        await update.message.reply_text("❌ You have no children")
        return
    
    children_text = "<b>👶 YOUR CHILDREN</b>\n\n"
    for child_id in family['children']:
        child = db.get_user(child_id)
        if child:
            children_text += f"• @{child['username']} (Level {child['level']})\n"
    
    await update.message.reply_text(children_text, parse_mode="HTML")

parents_handler = CommandHandler('parents', parents_command)
children_handler = CommandHandler('children', children_command)