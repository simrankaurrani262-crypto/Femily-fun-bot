"""
/question command - Answer questions for rewards
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import db
import random
import logging

logger = logging.getLogger(__name__)

QUIZ_QUESTIONS = [
    {
        "question": "What is 5 + 5?",
        "options": ["8", "10", "12", "15"],
        "correct": 1,
        "reward": 50,
        "emoji": "🔢"
    },
    {
        "question": "What is the color of the sky?",
        "options": ["Green", "Blue", "Red", "Yellow"],
        "correct": 1,
        "reward": 50,
        "emoji": "🌤️"
    },
    {
        "question": "How many days in a week?",
        "options": ["5", "6", "7", "8"],
        "correct": 2,
        "reward": 50,
        "emoji": "📅"
    },
    {
        "question": "What is 10 × 10?",
        "options": ["50", "75", "100", "150"],
        "correct": 2,
        "reward": 100,
        "emoji": "🔢"
    },
    {
        "question": "Capital of USA?",
        "options": ["New York", "Washington DC", "Los Angeles", "Chicago"],
        "correct": 1,
        "reward": 150,
        "emoji": "🇺🇸"
    },
    {
        "question": "What is the largest planet?",
        "options": ["Mars", "Saturn", "Jupiter", "Neptune"],
        "correct": 2,
        "reward": 100,
        "emoji": "🪐"
    },
]

async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask a question"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    question_data = random.choice(QUIZ_QUESTIONS)
    
    quiz_text = f"""
<b>❓ QUIZ QUESTION</b>

{question_data['emoji']} {question_data['question']}

<b>Reward:</b> {question_data['reward']} 💰
"""
    
    keyboard = []
    for idx, option in enumerate(question_data['options']):
        keyboard.append([
            InlineKeyboardButton(
                option,
                callback_data=f"quiz_{idx}_{question_data['correct']}_{question_data['reward']}_{user_id}"
            )
        ])
    
    context.user_data['quiz_question'] = question_data
    
    await update.message.reply_text(
        quiz_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Quiz question asked to {user_id}")

async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer"""
    query = update.callback_query
    await query.answer()
    
    try:
        data_parts = query.data.split('_')
        user_answer = int(data_parts[1])
        correct_answer = int(data_parts[2])
        reward = int(data_parts[3])
        user_id = int(data_parts[4])
        
        if user_id != update.effective_user.id:
            await query.edit_message_text("❌ This quiz is not for you!")
            return
        
        if user_answer == correct_answer:
            db.add_money(user_id, reward)
            await query.edit_message_text(
                f"✅ <b>CORRECT!</b>\n\n"
                f"💰 +{reward} coins earned!",
                parse_mode="HTML"
            )
            logger.info(f"Quiz: {user_id} answered correctly and earned {reward}")
        else:
            await query.edit_message_text(
                f"❌ <b>WRONG ANSWER</b>\n\n"
                f"Better luck next time!",
                parse_mode="HTML"
            )
            logger.info(f"Quiz: {user_id} answered incorrectly")
    except Exception as e:
        logger.error(f"Quiz error: {e}")
        await query.edit_message_text("❌ Error processing quiz")

question_handler = CommandHandler('question', question_command)
quiz_callback_handler = CallbackQueryHandler(quiz_callback, pattern="^quiz_")