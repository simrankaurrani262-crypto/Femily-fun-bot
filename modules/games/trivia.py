"""
/trivia command - Trivia game
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

TRIVIA_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "correct": 1,
        "reward": 100
    },
    {
        "question": "What is the largest planet?",
        "options": ["Mars", "Earth", "Jupiter", "Saturn"],
        "correct": 2,
        "reward": 100
    },
    {
        "question": "Who wrote Romeo and Juliet?",
        "options": ["Mark Twain", "Shakespeare", "Austen", "Dickens"],
        "correct": 1,
        "reward": 150
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct": 1,
        "reward": 50
    },
    {
        "question": "What year did World War II end?",
        "options": ["1943", "1944", "1945", "1946"],
        "correct": 2,
        "reward": 200
    },
]

async def trivia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play trivia"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Pick random question
    question_data = random.choice(TRIVIA_QUESTIONS)
    
    trivia_text = f"""
<b>❓ TRIVIA QUESTION</b>

{question_data['question']}
"""
    
    keyboard = []
    for idx, option in enumerate(question_data['options']):
        keyboard.append([InlineKeyboardButton(option, callback_data=f"trivia_{idx}_{question_data['correct']}_{question_data['reward']}")])
    
    context.user_data['trivia'] = question_data
    
    await update.message.reply_text(
        trivia_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

trivia_handler = CommandHandler('trivia', trivia_command)