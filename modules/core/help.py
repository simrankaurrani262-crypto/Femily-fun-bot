"""
/help command handler
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import logging

logger = logging.getLogger(__name__)

HELP_TEXT = """
<b>🎮 TELEGRAM RPG BOT - COMMAND HELP</b>

<b>📋 FAMILY TREE GAME QUICK MENU</b>
/menu - Open categorized menu
/me - Your full profile
/profile @user - View another user
/friends - Friend list
/removefriend @user - Remove friend
/balance - Check coins
/bet amount - Coin flip bet
/rps rock|paper|scissors - Mini game
/topmoney /topfamily /topgarden /topgames - Leaderboards
/enable /disable /reset - Group controls
/backup /restore - Data backup tools

<b>📌 CORE COMMANDS</b>
/start - Start the bot
/profile - View your profile
/stats - View your statistics
/help - Show this help message
/settings - Adjust settings

<b>👨‍👩‍👧‍👦 FAMILY COMMANDS</b>
/family - View family info
/tree - Generate family tree (IMAGE)
/fulltree - Full family tree with all relatives
/adopt - Adopt someone
/marry - Marry someone
/divorce - Divorce your partner
/disown - Disown a child
/parents - View parents
/children - View children

<b>👥 FRIEND COMMANDS</b>
/friend - Add friend
/unfriend - Remove friend
/circle - Friend circle
/ratings - Friend ratings
/suggestions - Friend suggestions

<b>💰 ECONOMY COMMANDS</b>
/daily - Claim daily reward (100 coins)
/account - View account balance
/pay @username amount - Pay another player
/deposit amount - Deposit to bank
/withdraw amount - Withdraw from bank
/job - View job info
/work - Work to earn money
/shop - View shop
/buy item_id - Buy an item
/inventory - View inventory
/bank - Bank information
/loan amount - Take a loan
/repay amount - Repay loan

<b>⚔️ CRIME COMMANDS</b>
/rob @username - Rob another player
/kill @username - Attack someone
/weapon - View weapons
/buyweapon - Buy a weapon
/insurance - View insurance
/medical - Get medical help
/jail - Check jail status
/bail - Pay to get out of jail

<b>🏭 FACTORY COMMANDS</b>
/factory - View your factory
/hire - Hire a worker
/fire - Fire a worker
/workers - View workers
/production - View production status
/factoryupgrade - Upgrade factory

<b>🌾 GARDEN COMMANDS</b>
/garden - View your garden
/add - Add a plot to garden
/plant seed_id - Plant a seed
/harvest - Harvest crops
/fertilise plot_id - Fertilise a plot
/barn - View barn storage
/orders - View orders
/seeds - View seed catalog
/weather - Check weather

<b>🛒 MARKET COMMANDS</b>
/stand - View your market stand
/stands - View all market stands
/putstand item_id amount price - Put item on stand
/trade - Trade with others
/gift @username item_id - Gift to someone
/auction - View auctions
/bid auction_id amount - Bid on auction

<b>🎲 GAMES COMMANDS</b>
/lottery - Lottery game
/blackjack - Play blackjack
/slots - Play slots
/dice - Roll dice
/trivia - Answer trivia
/guess - Guess number
/ripple - Ripple game
/question - Answer questions
/nation - Nation game
/4p - Four Pics One Word

<b>📊 LEADERBOARD COMMANDS</b>
/leaderboard - Top players
/moneyboard - Richest players
/familyboard - Largest families
/factoryboard - Best factories
/activity - Most active players
/moneygraph - Money graph

<b>⚙️ ADMIN COMMANDS</b> (Admins only)
/ban @username reason - Ban a user
/unban @username - Unban a user
/broadcast message - Send message to all users
/adminstats - View admin statistics
/logs - View bot logs

<b>📝 Tips:</b>
- Use /daily to earn coins every 24 hours
- Build a family to gain advantages
- Invest in a factory for passive income
- Check /leaderboard to compete with others
"""

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(HELP_TEXT, parse_mode="HTML")

help_handler = CommandHandler('help', help_command)
