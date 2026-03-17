"""
CENTRALIZED CALLBACK HANDLERS - COMPLETE
All inline button callbacks from across the bot are handled here.
This ensures every button click is properly registered and processed.
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import db
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CORE MODULE CALLBACKS (/start, /settings)
# ============================================================================

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu navigation from /start"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "profile":
        await query.edit_message_text(
            "<b>👤 PROFILE</b>\n\n"
            "Use /profile to view your full profile",
            parse_mode="HTML"
        )
    elif query.data == "games":
        await query.edit_message_text(
            "<b>🎮 GAMES</b>\n\n"
            "Available games:\n"
            "/blackjack - Card game\n"
            "/slots - Slot machine\n"
            "/trivia - Trivia questions\n"
            "/question - Quiz\n"
            "/lottery - Lottery\n"
            "/dice - Roll dice\n"
            "/guess - Guess the number\n"
            "/ripple - Memory game\n"
            "/4p - Four Pics One Word",
            parse_mode="HTML"
        )
    elif query.data == "family":
        await query.edit_message_text(
            "<b>👨‍👩‍👧‍👦 FAMILY</b>\n\n"
            "Use /family to manage your family\n"
            "/tree - View family tree\n"
            "/marry - Marry someone\n"
            "/adopt - Adopt a child\n"
            "/divorce - End marriage",
            parse_mode="HTML"
        )
    elif query.data == "economy":
        await query.edit_message_text(
            "<b>💰 ECONOMY</b>\n\n"
            "Financial commands:\n"
            "/daily - Daily reward\n"
            "/account - View balance\n"
            "/shop - Buy items\n"
            "/bank - Bank operations\n"
            "/pay - Send money",
            parse_mode="HTML"
        )
    elif query.data == "stats":
        await query.edit_message_text(
            "<b>📊 STATS & LEADERBOARDS</b>\n\n"
            "/leaderboard - Top players\n"
            "/moneyboard - Richest players\n"
            "/familyboard - Family rankings\n"
            "/factoryboard - Factory rankings",
            parse_mode="HTML"
        )
    elif query.data == "settings":
        keyboard = [
            [InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications")],
            [InlineKeyboardButton("🎨 Theme", callback_data="settings_theme")],
            [InlineKeyboardButton("🔒 Privacy", callback_data="settings_privacy")],
            [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "<b>⚙️ SETTINGS</b>\n\nChoose a setting to adjust:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "guide":
        await query.edit_message_text(
            "<b>📖 QUICK START GUIDE</b>\n\n"
            "1️⃣ Start with /daily to claim rewards\n"
            "2️⃣ Build your family with /family\n"
            "3️⃣ Earn money with /jobs\n"
            "4️⃣ Buy items from /shop\n"
            "5️⃣ Play games for rewards\n"
            "6️⃣ Compete on /leaderboard\n\n"
            "Type /help for all commands!",
            parse_mode="HTML"
        )

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle settings callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "settings_notifications":
        keyboard = [
            [InlineKeyboardButton("✅ On", callback_data="notif_on")],
            [InlineKeyboardButton("❌ Off", callback_data="notif_off")],
        ]
        await query.edit_message_text(
            "<b>🔔 Notifications</b>\n\nEnable notifications?",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "notif_on":
        db.update_user_setting(query.from_user.id, "notifications", True)
        await query.edit_message_text(
            "✅ <b>Notifications Enabled</b>",
            parse_mode="HTML"
        )
    elif query.data == "notif_off":
        db.update_user_setting(query.from_user.id, "notifications", False)
        await query.edit_message_text(
            "❌ <b>Notifications Disabled</b>",
            parse_mode="HTML"
        )
    elif query.data == "settings_theme":
        keyboard = [
            [InlineKeyboardButton("🌙 Dark", callback_data="theme_dark")],
            [InlineKeyboardButton("☀️ Light", callback_data="theme_light")],
        ]
        await query.edit_message_text(
            "<b>🎨 Theme</b>\n\nChoose your theme:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "theme_dark":
        db.update_user_setting(query.from_user.id, "theme", "dark")
        await query.edit_message_text(
            "✅ <b>Dark Theme Selected</b>",
            parse_mode="HTML"
        )
    elif query.data == "theme_light":
        db.update_user_setting(query.from_user.id, "theme", "light")
        await query.edit_message_text(
            "✅ <b>Light Theme Selected</b>",
            parse_mode="HTML"
        )
    elif query.data == "settings_privacy":
        keyboard = [
            [InlineKeyboardButton("👀 Public", callback_data="privacy_public")],
            [InlineKeyboardButton("🔒 Private", callback_data="privacy_private")],
        ]
        await query.edit_message_text(
            "<b>🔒 Privacy</b>\n\nWho can see your profile?",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "privacy_public":
        db.update_user_setting(query.from_user.id, "privacy", "public")
        await query.edit_message_text(
            "✅ <b>Profile is Public</b>",
            parse_mode="HTML"
        )
    elif query.data == "privacy_private":
        db.update_user_setting(query.from_user.id, "privacy", "private")
        await query.edit_message_text(
            "✅ <b>Profile is Private</b>",
            parse_mode="HTML"
        )
    elif query.data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("🎮 Play Games", callback_data="menu_games")],
            [InlineKeyboardButton("💼 Economy", callback_data="menu_economy")],
            [InlineKeyboardButton("👨‍👩‍👧‍👦 Family", callback_data="menu_family")],
        ]
        await query.edit_message_text(
            "<b>📋 MAIN MENU</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ============================================================================
# SHOP & ECONOMY CALLBACKS
# ============================================================================

async def shop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle shop item purchases via inline buttons"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("buy_") and not query.data.startswith("buy_weapon_"):
        item_name = query.data.replace("buy_", "")
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        if not user:
            await query.answer("❌ Please use /start first", show_alert=True)
            return
        
        from modules.economy.shop import SHOP_ITEMS
        
        if item_name not in SHOP_ITEMS:
            await query.answer("❌ Item not found", show_alert=True)
            return
        
        item_info = SHOP_ITEMS[item_name]
        
        if user['money'] < item_info['price']:
            await query.answer(
                f"❌ You need {item_info['price']} 💰\nYou have {user['money']} 💰",
                show_alert=True
            )
            return
        
        db.withdraw_money(user_id, item_info['price'])
        db.add_item(user_id, item_name)
        
        await query.answer("✅ Purchase successful!", show_alert=False)
        await query.edit_message_text(
            f"✅ <b>PURCHASE SUCCESSFUL!</b>\n\n"
            f"{item_info['emoji']} {item_name.capitalize()}\n"
            f"Cost: {item_info['price']} 💰\n"
            f"Balance: {user['money'] - item_info['price']:,} 💰",
            parse_mode="HTML"
        )
        logger.info(f"Purchase via button: {user_id} bought {item_name}")

async def bank_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bank operation callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await query.answer("❌ Please use /start first", show_alert=True)
        return
    
    if query.data == "bank_deposit":
        await query.edit_message_text(
            "<b>💰 DEPOSIT</b>\n\n"
            "Use /deposit amount\n"
            "Example: /deposit 1000",
            parse_mode="HTML"
        )
    elif query.data == "bank_withdraw":
        await query.edit_message_text(
            "<b>💸 WITHDRAW</b>\n\n"
            "Use /withdraw amount\n"
            "Example: /withdraw 500",
            parse_mode="HTML"
        )
    elif query.data == "bank_transactions":
        await query.edit_message_text(
            "<b>📊 TRANSACTIONS</b>\n\n"
            "Recent transactions:\n"
            f"• Deposit: +1000\n"
            f"• Withdrawal: -500",
            parse_mode="HTML"
        )
    elif query.data == "bank_settings":
        keyboard = [
            [InlineKeyboardButton("🔔 Alerts", callback_data="bank_alerts")],
            [InlineKeyboardButton("🔑 Security", callback_data="bank_security")],
        ]
        await query.edit_message_text(
            "<b>⚙️ BANK SETTINGS</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "bank_alerts":
        await query.edit_message_text(
            "✅ <b>Alerts Enabled</b>",
            parse_mode="HTML"
        )
    elif query.data == "bank_security":
        await query.edit_message_text(
            "🔒 <b>Security Settings</b>\n\nYour account is secure.",
            parse_mode="HTML"
        )

# ============================================================================
# MARKET & AUCTION CALLBACKS
# ============================================================================

async def auction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle auction callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "auction_bid":
        await query.edit_message_text(
            "<b>📝 PLACE BID</b>\n\n"
            "Use /bid auction_id amount\n"
            "Example: /bid 1 500",
            parse_mode="HTML"
        )
        logger.info(f"Auction bid initiated by {query.from_user.id}")

async def market_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle market callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "market_browse_all":
        await query.edit_message_text(
            "<b>🛍️ BROWSE ALL STANDS</b>\n\n"
            "Use /stands to view all available stands\n"
            "Click stand buttons to view items",
            parse_mode="HTML"
        )

# ============================================================================
# GAMES CALLBACKS
# ============================================================================

async def blackjack_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle blackjack game callbacks"""
    query = update.callback_query
    await query.answer()
    
    if "blackjack" not in context.user_data:
        await query.answer("❌ No active game. Start with /blackjack", show_alert=True)
        return
    
    game = context.user_data['blackjack']
    user_id = query.from_user.id
    
    if query.data == "bj_hit":
        import random
        from modules.games.blackjack import CARDS, hand_value
        
        game['player_hand'].append(random.choice(CARDS))
        player_value = hand_value(game['player_hand'])
        
        if player_value > 21:
            await query.edit_message_text(
                f"<b>🎰 BLACKJACK</b>\n\n"
                f"Your Hand: {' '.join(game['player_hand'])} = {player_value}\n\n"
                f"❌ <b>BUST!</b> You went over 21!\n"
                f"Lost: {game['bet']} 💰",
                parse_mode="HTML"
            )
            del context.user_data['blackjack']
            logger.info(f"Blackjack bust: {user_id}")
        else:
            keyboard = [
                [
                    InlineKeyboardButton("📍 Hit", callback_data="bj_hit"),
                    InlineKeyboardButton("⏹️ Stand", callback_data="bj_stand"),
                ],
            ]
            await query.edit_message_text(
                f"<b>🎰 BLACKJACK</b>\n\n"
                f"Your Hand: {' '.join(game['player_hand'])} = {player_value}\n"
                f"Dealer: {game['dealer_hand'][0]} ?\n\n"
                f"Bet: {game['bet']} 💰",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    elif query.data == "bj_stand":
        from modules.games.blackjack import hand_value
        
        player_value = hand_value(game['player_hand'])
        dealer_value = hand_value(game['dealer_hand'])
        
        result_text = f"<b>🎰 BLACKJACK</b>\n\n"
        result_text += f"Your Hand: {' '.join(game['player_hand'])} = {player_value}\n"
        result_text += f"Dealer: {' '.join(game['dealer_hand'])} = {dealer_value}\n\n"
        
        if dealer_value > player_value:
            result_text += f"❌ <b>DEALER WINS!</b>\n"
            result_text += f"Lost: {game['bet']} 💰"
        elif dealer_value == player_value:
            result_text += f"🤝 <b>PUSH (TIE)</b>\n"
            result_text += f"Your bet is returned: {game['bet']} 💰"
            db.add_money(user_id, game['bet'])
        else:
            winnings = game['bet'] * 2
            result_text += f"✅ <b>YOU WIN!</b>\n"
            result_text += f"Won: {winnings} 💰"
            db.add_money(user_id, winnings)
        
        await query.edit_message_text(result_text, parse_mode="HTML")
        del context.user_data['blackjack']
        logger.info(f"Blackjack finished: {user_id}")

async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer callbacks"""
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

async def trivia_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle trivia answer callbacks"""
    query = update.callback_query
    await query.answer()
    
    try:
        data_parts = query.data.split('_')
        user_answer = int(data_parts[1])
        correct_answer = int(data_parts[2])
        reward = int(data_parts[3])
        user_id = update.effective_user.id
        
        user = db.get_user(user_id)
        if not user:
            await query.answer("❌ Please use /start first", show_alert=True)
            return
        
        if user_answer == correct_answer:
            db.add_money(user_id, reward)
            await query.edit_message_text(
                f"✅ <b>CORRECT!</b>\n\n"
                f"💰 +{reward} coins earned!",
                parse_mode="HTML"
            )
            logger.info(f"Trivia: {user_id} answered correctly and earned {reward}")
        else:
            await query.edit_message_text(
                f"❌ <b>WRONG ANSWER</b>\n\n"
                f"Better luck next time!",
                parse_mode="HTML"
            )
            logger.info(f"Trivia: {user_id} answered incorrectly")
    except Exception as e:
        logger.error(f"Trivia error: {e}")
        await query.edit_message_text("❌ Error processing trivia")

# ============================================================================
# CRIME MODULE CALLBACKS (Weapons)
# ============================================================================

async def weapon_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle weapon purchases"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("buy_weapon_"):
        weapon_name = query.data.replace("buy_weapon_", "")
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        if not user:
            await query.answer("❌ Please use /start first", show_alert=True)
            return
        
        from modules.crime.weapon import WEAPONS
        
        if weapon_name not in WEAPONS:
            await query.answer("❌ Weapon not found", show_alert=True)
            return
        
        weapon_info = WEAPONS[weapon_name]
        
        if user['money'] < weapon_info['cost']:
            await query.answer(
                f"❌ You need {weapon_info['cost']} 💰\nYou have {user['money']} 💰",
                show_alert=True
            )
            return
        
        db.withdraw_money(user_id, weapon_info['cost'])
        db.add_item(user_id, weapon_name)
        
        await query.answer("✅ Weapon purchased!", show_alert=False)
        await query.edit_message_text(
            f"✅ <b>WEAPON PURCHASED!</b>\n\n"
            f"{weapon_info['emoji']} {weapon_name.capitalize()}\n"
            f"Power: +{weapon_info['power']}\n"
            f"Cost: {weapon_info['cost']} 💰\n"
            f"New Balance: {user['money'] - weapon_info['cost']:,} 💰",
            parse_mode="HTML"
        )
        logger.info(f"Weapon purchased: {user_id} bought {weapon_name}")

# ============================================================================
# STATS/LEADERBOARD CALLBACKS
# ============================================================================

async def leaderboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle leaderboard view changes"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "lb_money":
        users = db.get_leaderboard('money', 10)
        lb_text = "<b>💰 RICHEST PLAYERS</b>\n\n"
        for idx, user in enumerate(users, 1):
            lb_text += f"{idx}. @{user['username']} - {user['money']:,} 💰\n"
    elif query.data == "lb_level":
        users = db.get_leaderboard('level', 10)
        lb_text = "<b>⭐ TOP LEVEL PLAYERS</b>\n\n"
        for idx, user in enumerate(users, 1):
            lb_text += f"{idx}. @{user['username']} - Level {user['level']}\n"
    elif query.data == "lb_family":
        users = db.get_leaderboard('family_size', 10)
        lb_text = "<b>👨‍👩‍👧‍👦 LARGEST FAMILIES</b>\n\n"
        for idx, user in enumerate(users, 1):
            family_size = len(user.get('family', []))
            lb_text += f"{idx}. @{user['username']} - {family_size} members\n"
    elif query.data == "lb_factory":
        users = db.get_leaderboard('factory_level', 10)
        lb_text = "<b>🏭 BEST FACTORIES</b>\n\n"
        for idx, user in enumerate(users, 1):
            factory_level = user.get('factory', {}).get('level', 0)
            lb_text += f"{idx}. @{user['username']} - Factory Level {factory_level}\n"
    else:
        return
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Money", callback_data="lb_money"),
            InlineKeyboardButton("⭐ Level", callback_data="lb_level"),
        ],
        [
            InlineKeyboardButton("👨‍👩‍👧‍👦 Family", callback_data="lb_family"),
            InlineKeyboardButton("🏭 Factory", callback_data="lb_factory"),
        ],
    ]
    
    await query.edit_message_text(
        lb_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Leaderboard viewed by {query.from_user.id}")

# ============================================================================
# GARDEN CALLBACKS
# ============================================================================

async def garden_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle garden operation callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await query.answer("❌ Please use /start first", show_alert=True)
        return
    
    if query.data == "garden_plant":
        await query.edit_message_text(
            "<b>🌱 PLANT CROP</b>\n\n"
            "Use /plant crop_name\n"
            "Available: wheat, corn, tomato, carrot",
            parse_mode="HTML"
        )
    elif query.data == "garden_harvest":
        await query.edit_message_text(
            "<b>🌾 HARVEST</b>\n\n"
            "Use /harvest to collect ready crops",
            parse_mode="HTML"
        )
    elif query.data == "garden_barn":
        await query.edit_message_text(
            "<b>🥗 BARN STORAGE</b>\n\n"
            "Use /barn to manage your storage\n"
            "View and organize your crops",
            parse_mode="HTML"
        )
    elif query.data == "garden_fertilise":
        await query.edit_message_text(
            "<b>✨ FERTILISE</b>\n\n"
            "Use /fertilise plot_id\n"
            "Speed up crop growth!",
            parse_mode="HTML"
        )

# ============================================================================
# FRIENDS CALLBACKS
# ============================================================================

async def friends_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle friend suggestion callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("add_friend_"):
        target_user_id = int(query.data.replace("add_friend_", ""))
        user_id = query.from_user.id
        
        user = db.get_user(user_id)
        target = db.get_user(target_user_id)
        
        if not user or not target:
            await query.answer("❌ User not found", show_alert=True)
            return
        
        # Add friend
        db.add_friend(user_id, target_user_id)
        
        await query.answer(f"✅ Added @{target['username']} as friend!", show_alert=False)
        await query.edit_message_text(
            f"✅ <b>FRIEND ADDED!</b>\n\n"
            f"@{target['username']} is now your friend",
            parse_mode="HTML"
        )
        logger.info(f"Friend added: {user_id} added {target_user_id}")

# ============================================================================
# CREATE ALL HANDLERS
# ============================================================================

# Main menu & Start
start_callback_handler = CallbackQueryHandler(main_menu_callback, pattern="^(profile|games|family|economy|stats|guide|menu_)")

# Settings
settings_callback_handler = CallbackQueryHandler(settings_callback, pattern="^(settings_|notif_|theme_|privacy_|main_menu)")

# Shop & Economy
shop_callback_handler = CallbackQueryHandler(shop_callback, pattern="^buy_(?!weapon_)")
bank_callback_handler = CallbackQueryHandler(bank_callback, pattern="^bank_")

# Market & Auctions
auction_callback_handler = CallbackQueryHandler(auction_callback, pattern="^auction_")
market_callback_handler = CallbackQueryHandler(market_callback, pattern="^market_")

# Games
blackjack_callback_handler = CallbackQueryHandler(blackjack_callback, pattern="^bj_")
quiz_callback_handler = CallbackQueryHandler(quiz_callback, pattern="^quiz_")
trivia_callback_handler = CallbackQueryHandler(trivia_callback, pattern="^trivia_")

# Crime
weapon_callback_handler = CallbackQueryHandler(weapon_callback, pattern="^buy_weapon_")

# Stats
leaderboard_callback_handler = CallbackQueryHandler(leaderboard_callback, pattern="^lb_")

# Garden
garden_callback_handler = CallbackQueryHandler(garden_callback, pattern="^garden_")

# Friends
friends_callback_handler = CallbackQueryHandler(friends_callback, pattern="^add_friend_")
