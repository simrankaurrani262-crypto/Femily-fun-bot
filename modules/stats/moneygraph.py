"""
/moneygraph command - Generate money chart
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import matplotlib.pyplot as plt
import matplotlib
import io
import logging

logger = logging.getLogger(__name__)

matplotlib.use('Agg')

async def moneygraph_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate money graph"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Pie chart: Wallet vs Bank
    labels = ['Wallet', 'Bank']
    sizes = [user['money'], user['bank']]
    colors = ['#FFD700', '#4169E1']
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Wallet vs Bank Balance')
    
    # Bar chart: Money comparison with leaderboard
    top_users = db.get_leaderboard('money', 5)
    names = [db.get_user(u['user_id'])['username'][:10] if db.get_user(u['user_id']) else 'Unknown' 
             for u in top_users]
    money = [u['money'] for u in top_users]
    
    ax2.bar(names, money, color='#32CD32')
    ax2.set_title('Top 5 Richest Players')
    ax2.set_ylabel('Money (💰)')
    plt.xticks(rotation=45)
    
    # Save to bytes
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    plt.close()
    buf.seek(0)
    
    # Send graph
    caption = f"""
Your Money: {user['money']:,} 💰
Bank Balance: {user['bank']:,} 💰
Total: {user['money'] + user['bank']:,} 💰
"""
    
    await update.message.reply_photo(photo=buf, caption=caption)
    logger.info(f"Money graph generated for {user_id}")

moneygraph_handler = CommandHandler('moneygraph', moneygraph_command)