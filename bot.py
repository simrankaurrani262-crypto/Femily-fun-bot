"""
COMPLETE TELEGRAM RPG BOT - MAIN ENTRY POINT
All 84+ Commands Fully Registered + ALL BUTTONS
Fixed and Enhanced Version
"""
import asyncio
import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN, LOG_LEVEL, WEBHOOK_URL, WEBHOOK_PORT
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run).start()

# Setup logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
os.makedirs('logs', exist_ok=True)

# ============================================================================
# IMPORT ALL COMMAND HANDLERS
# ============================================================================

# Core
from modules.core.start import start_handler
from modules.core.help import help_handler
from modules.core.profile import profile_handler
from modules.core.settings import settings_handler
from modules.core.stats import stats_handler
from modules.core.masterplus import masterplus_handlers, requests_callback_handler

# Family
from modules.family.family import family_handler
from modules.family.tree import tree_handler
from modules.family.tree import fulltree_handler
from modules.family.marry import marry_handler
from modules.family.divorce import divorce_handler
from modules.family.adopt import adopt_handler
from modules.family.disown import disown_handler
from modules.family.relations import parents_handler, children_handler

# Friends
from modules.friends.friend import friend_handler
from modules.friends.unfriend import unfriend_handler
from modules.friends.circle import circle_handler
from modules.friends.ratings import ratings_handler
from modules.friends.suggestions import suggestions_handler

# Economy
from modules.economy.daily import daily_handler
from modules.economy.account import account_handler
from modules.economy.pay import pay_handler
from modules.economy.deposit import deposit_handler
from modules.economy.withdraw import withdraw_handler
from modules.economy.jobs import job_handler, work_handler
from modules.economy.inventory import inventory_handler
from modules.economy.shop import shop_handler, buy_handler
from modules.economy.bank import bank_handler
from modules.economy.loan import loan_handler, repay_handler

# Crime
from modules.crime.rob import rob_handler
from modules.crime.kill import kill_handler
from modules.crime.weapon import weapon_handler, buyweapon_handler
from modules.crime.insurance import insurance_handler
from modules.crime.medical import medical_handler
from modules.crime.jail import jail_handler
from modules.crime.bail import bail_handler

# Factory
from modules.factory.factory import factory_handler
from modules.factory.hire import hire_handler
from modules.factory.fire import fire_handler
from modules.factory.workers import workers_handler
from modules.factory.production import production_handler
from modules.factory.factoryupgrade import factoryupgrade_handler

# Garden
from modules.garden.garden import garden_handler
from modules.garden.add import add_handler
from modules.garden.plant import plant_handler
from modules.garden.harvest import harvest_handler
from modules.garden.fertilise import fertilise_handler
from modules.garden.barn import barn_handler
from modules.garden.orders import orders_handler
from modules.garden.seeds import seeds_handler
from modules.garden.weather import weather_handler

# Market
from modules.market.stand import stand_handler
from modules.market.stands import stands_handler
from modules.market.putstand import putstand_handler
from modules.market.trade import trade_handler
from modules.market.gift import gift_handler
from modules.market.auction import auction_handler
from modules.market.bid import bid_handler

# Games
from modules.games.lottery import lottery_handler
from modules.games.blackjack import blackjack_handler
from modules.games.slots import slots_handler
from modules.games.dice import dice_handler
from modules.games.trivia import trivia_handler
from modules.games.guess import guess_handler
from modules.games.ripple import ripple_handler
from modules.games.quiz import question_handler
from modules.games.nation import nation_handler
from modules.games.fourpics import fourpics_handler

# Stats
from modules.stats.leaderboard import leaderboard_handler
from modules.stats.moneyboard import moneyboard_handler
from modules.stats.familyboard import familyboard_handler
from modules.stats.factoryboard import factoryboard_handler
from modules.stats.activity import activity_handler
from modules.stats.moneygraph import moneygraph_handler

# Admin
from modules.admin.ban import ban_handler
from modules.admin.unban import unban_handler
from modules.admin.broadcast import broadcast_handler
from modules.admin.adminstats import adminstats_handler
from modules.admin.logs import logs_handler

# ============================================================================
# IMPORT ALL CALLBACK HANDLERS (CENTRALIZED)
# ============================================================================
from modules.callbacks import (
    start_callback_handler,
    settings_callback_handler,
    shop_callback_handler,
    bank_callback_handler,
    auction_callback_handler,
    market_callback_handler,
    blackjack_callback_handler,
    quiz_callback_handler,
    trivia_callback_handler,
    weapon_callback_handler,
    leaderboard_callback_handler,
    garden_callback_handler,
    friends_callback_handler,
    marriage_callback_handler,
    adopt_callback_handler,
)

# ============================================================================
# MAIN BOT FUNCTION
# ============================================================================

def main():
    """Start the bot"""
    logger.info("=" * 80)
    logger.info("🤖 TELEGRAM RPG BOT - STARTING")
    logger.info("=" * 80)
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).concurrent_updates(True).build()
    
    logger.info("")
    logger.info("📝 Registering command handlers...")
    logger.info("")

    # MASTER+ OVERRIDES / REQUIRED COMMAND ALIASES
    for handler in masterplus_handlers:
        app.add_handler(handler, group=-1)
    app.add_handler(requests_callback_handler, group=-1)
    logger.info("✅ MASTER+: aliases, requests, group controls")
    
    # CORE (6)
    app.add_handler(start_handler)
    app.add_handler(help_handler)
    app.add_handler(profile_handler)
    app.add_handler(settings_handler)
    app.add_handler(stats_handler)
    logger.info("✅ CORE: 6 commands")
    
    # FAMILY (9)
    app.add_handler(family_handler)
    app.add_handler(tree_handler)
    app.add_handler(fulltree_handler)
    app.add_handler(marry_handler)
    app.add_handler(divorce_handler)
    app.add_handler(adopt_handler)
    app.add_handler(disown_handler)
    app.add_handler(parents_handler)
    app.add_handler(children_handler)
    logger.info("✅ FAMILY: 9 commands")
    
    # FRIENDS (5)
    app.add_handler(friend_handler)
    app.add_handler(unfriend_handler)
    app.add_handler(circle_handler)
    app.add_handler(ratings_handler)
    app.add_handler(suggestions_handler)
    logger.info("✅ FRIENDS: 5 commands")
    
    # ECONOMY (13)
    app.add_handler(daily_handler)
    app.add_handler(account_handler)
    app.add_handler(pay_handler)
    app.add_handler(deposit_handler)
    app.add_handler(withdraw_handler)
    app.add_handler(job_handler)
    app.add_handler(work_handler)
    app.add_handler(inventory_handler)
    app.add_handler(shop_handler)
    app.add_handler(buy_handler)
    app.add_handler(bank_handler)
    app.add_handler(loan_handler)
    app.add_handler(repay_handler)
    logger.info("✅ ECONOMY: 13 commands")
    
    # CRIME (8)
    app.add_handler(rob_handler)
    app.add_handler(kill_handler)
    app.add_handler(weapon_handler)
    app.add_handler(buyweapon_handler)
    app.add_handler(insurance_handler)
    app.add_handler(medical_handler)
    app.add_handler(jail_handler)
    app.add_handler(bail_handler)
    logger.info("✅ CRIME: 8 commands")
    
    # FACTORY (6)
    app.add_handler(factory_handler)
    app.add_handler(hire_handler)
    app.add_handler(fire_handler)
    app.add_handler(workers_handler)
    app.add_handler(production_handler)
    app.add_handler(factoryupgrade_handler)
    logger.info("✅ FACTORY: 6 commands")
    
    # GARDEN (9)
    app.add_handler(garden_handler)
    app.add_handler(add_handler)
    app.add_handler(plant_handler)
    app.add_handler(harvest_handler)
    app.add_handler(fertilise_handler)
    app.add_handler(barn_handler)
    app.add_handler(orders_handler)
    app.add_handler(seeds_handler)
    app.add_handler(weather_handler)
    logger.info("✅ GARDEN: 9 commands")
    
    # MARKET (7)
    app.add_handler(stand_handler)
    app.add_handler(stands_handler)
    app.add_handler(putstand_handler)
    app.add_handler(trade_handler)
    app.add_handler(gift_handler)
    app.add_handler(auction_handler)
    app.add_handler(bid_handler)
    logger.info("✅ MARKET: 7 commands")
    
    # GAMES (10)
    app.add_handler(lottery_handler)
    app.add_handler(blackjack_handler)
    app.add_handler(slots_handler)
    app.add_handler(dice_handler)
    app.add_handler(trivia_handler)
    app.add_handler(guess_handler)
    app.add_handler(ripple_handler)
    app.add_handler(question_handler)
    app.add_handler(nation_handler)
    app.add_handler(fourpics_handler)
    logger.info("✅ GAMES: 10 commands")
    
    # STATS (6)
    app.add_handler(leaderboard_handler)
    app.add_handler(moneyboard_handler)
    app.add_handler(familyboard_handler)
    app.add_handler(factoryboard_handler)
    app.add_handler(activity_handler)
    app.add_handler(moneygraph_handler)
    logger.info("✅ STATS: 6 commands")
    
    # ADMIN (5)
    app.add_handler(ban_handler)
    app.add_handler(unban_handler)
    app.add_handler(broadcast_handler)
    app.add_handler(adminstats_handler)
    app.add_handler(logs_handler)
    logger.info("✅ ADMIN: 5 commands")
    
    logger.info("")
    logger.info("=" * 80)
    logger.info("📝 Registering callback handlers (INLINE BUTTONS)...")
    logger.info("")
    
    # CALLBACK HANDLERS
    app.add_handler(start_callback_handler)
    logger.info("✅ Start menu callbacks")
    
    app.add_handler(settings_callback_handler)
    logger.info("✅ Settings callbacks")
    
    app.add_handler(shop_callback_handler)
    logger.info("✅ Shop callbacks")
    
    app.add_handler(bank_callback_handler)
    logger.info("✅ Bank callbacks")
    
    app.add_handler(auction_callback_handler)
    logger.info("✅ Auction callbacks")
    
    app.add_handler(market_callback_handler)
    logger.info("✅ Market callbacks")
    
    app.add_handler(blackjack_callback_handler)
    logger.info("✅ Blackjack callbacks")
    
    app.add_handler(quiz_callback_handler)
    logger.info("✅ Quiz callbacks")
    
    app.add_handler(trivia_callback_handler)
    logger.info("✅ Trivia callbacks")
    
    app.add_handler(weapon_callback_handler)
    logger.info("✅ Weapon callbacks")
    
    app.add_handler(leaderboard_callback_handler)
    logger.info("✅ Leaderboard callbacks")
    
    app.add_handler(garden_callback_handler)
    logger.info("✅ Garden callbacks")
    
    app.add_handler(friends_callback_handler)
    logger.info("✅ Friends callbacks")
    
    app.add_handler(marriage_callback_handler)
    logger.info("✅ Marriage callbacks")
    
    app.add_handler(adopt_callback_handler)
    logger.info("✅ Adoption callbacks")
    
    logger.info("")
    logger.info("=" * 80)
    logger.info("✅ ALL 84+ COMMAND HANDLERS REGISTERED!")
    logger.info("✅ ALL 15 CALLBACK MODULES REGISTERED!")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📊 SUMMARY:")
    logger.info("   Core: 6  | Family: 9 | Friends: 5")
    logger.info("   Economy: 13 | Crime: 8 | Factory: 6")
    logger.info("   Garden: 9 | Market: 7 | Games: 10 | Stats: 6 | Admin: 5")
    logger.info("   ──────────────────────────────────")
    logger.info("   TOTAL: 84+ COMMANDS")
    logger.info("")
    logger.info("🚀 BOT IS RUNNING AND READY!")
    logger.info("")
    
    if WEBHOOK_URL:
        logger.info(f"🌐 Running in webhook mode on port {WEBHOOK_PORT}")
        app.run_webhook(
            listen="0.0.0.0",
            port=WEBHOOK_PORT,
            url_path=TELEGRAM_TOKEN,
            webhook_url=f"{WEBHOOK_URL.rstrip('/')}/{TELEGRAM_TOKEN}",
            allowed_updates=['message', 'callback_query'],
        )
    else:
        logger.info("📡 Running in polling mode")
        app.run_polling(allowed_updates=['message', 'callback_query'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Critical error: {e}", exc_info=True)
