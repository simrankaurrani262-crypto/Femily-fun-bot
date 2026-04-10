"""
Master+ feature pack for Family Tree Game Bot.
Adds command aliases, advanced requests, group moderation toggles, and menu UX.
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import db
from modules.utils.group_handler import get_target_user, get_display_name
import random
from pathlib import Path

REQUEST_PREFIX = "req"


def _is_group(chat):
    return chat.type in ("group", "supergroup")


async def _ensure_registered(update: Update):
    chat = update.effective_chat
    if _is_group(chat) and not db.is_group_enabled(chat.id):
        await update.message.reply_text("⛔ Bot is disabled in this group. Admins can use /enable.")
        return None
    user = db.get_user(update.effective_user.id)
    if not user:
        await update.message.reply_text("❌ Please use /start first to register.")
        return None
    return user


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "<b>🌳 Family Tree Game Bot - Main Menu</b>\n\n"
        "<b>Core:</b> /start /help /me /profile /stats\n"
        "<b>Family:</b> /marry /divorce /adopt /parents /children /siblings /tree\n"
        "<b>Social:</b> /friend /friends /removefriend\n"
        "<b>Economy:</b> /balance /daily /work /pay\n"
        "<b>Garden:</b> /garden /plant /water /harvest\n"
        "<b>Games:</b> /lottery /bet /dice /rps /nation\n"
        "<b>Top:</b> /topmoney /topfamily /topgarden /topgames\n"
        "<b>Group Admin:</b> /enable /disable /reset /ban"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def set_commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = [
        BotCommand("start", "Register / Start"),
        BotCommand("help", "All commands"),
        BotCommand("menu", "Open command menu"),
        BotCommand("me", "My profile"),
        BotCommand("profile", "View user profile"),
        BotCommand("marry", "Send marriage proposal"),
        BotCommand("adopt", "Send adoption request"),
        BotCommand("friend", "Send friend request"),
        BotCommand("garden", "View garden"),
        BotCommand("balance", "Check coins"),
        BotCommand("daily", "Daily reward"),
        BotCommand("work", "Work for coins"),
        BotCommand("pay", "Pay another user"),
    ]
    await context.bot.set_my_commands(commands)
    await update.message.reply_text("✅ Bot command menu updated.")


async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    family = db.get_family(user["user_id"]) or {}
    garden = db.db.gardens.find_one({"user_id": user["user_id"]}) or {}
    text = (
        f"<b>👤 {get_display_name(user)} - Profile</b>\n\n"
        f"🆔 <b>ID:</b> <code>{user['user_id']}</code>\n"
        f"🚻 <b>Gender:</b> {user.get('gender', 'unknown')}\n"
        f"🎂 <b>Age:</b> {user.get('age', 'N/A')}\n"
        f"💍 <b>Status:</b> {user.get('status', 'single')}\n"
        f"❤️ <b>Partner:</b> {family.get('partner') or 'None'}\n"
        f"👶 <b>Children:</b> {len(family.get('children', []))}\n"
        f"💰 <b>Money:</b> {user.get('money', 0):,}\n"
        f"⭐ <b>Level:</b> {user.get('level', 1)}\n"
        f"🌱 <b>Garden Plots:</b> {len(garden.get('plots', []))}\n"
        f"📊 <b>Stats:</b> XP {user.get('xp', 0)} / Rep {user.get('reputation', 0)}"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def profile_lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await me_command(update, context)
    username = context.args[0].lstrip("@")
    target = db.get_user_by_username(username)
    if not target:
        return await update.message.reply_text("❌ User not found.")
    family = db.get_family(target["user_id"]) or {}
    await update.message.reply_text(
        f"<b>👤 @{target.get('username', target['user_id'])}</b>\n"
        f"💰 {target.get('money', 0):,} | ⭐ {target.get('level', 1)}\n"
        f"💍 Status: {target.get('status', 'single')} | 👶 Children: {len(family.get('children', []))}",
        parse_mode="HTML"
    )


async def _request_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, kind: str, prompt: str):
    user = await _ensure_registered(update)
    if not user:
        return

    target_user_id, target_name, error = await get_target_user(update, context)
    if error:
        return await update.message.reply_text(f"❌ {error}")

    if target_user_id == user["user_id"]:
        return await update.message.reply_text("❌ You cannot target yourself.")
    if kind == "marry":
        my_family = db.get_family(user["user_id"]) or {}
        target_family = db.get_family(target_user_id) or {}
        if my_family.get("partner") or target_family.get("partner"):
            return await update.message.reply_text("❌ One of you is already married.")
        if target_user_id in my_family.get("parents", []) or target_user_id in my_family.get("children", []):
            return await update.message.reply_text("❌ Invalid relation: you cannot marry direct family members.")
    if kind == "adopt":
        my_family = db.get_family(user["user_id"]) or {}
        if target_user_id in my_family.get("parents", []):
            return await update.message.reply_text("❌ Circular relation blocked.")

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Accept", callback_data=f"{REQUEST_PREFIX}:{kind}:accept:{user['user_id']}:{target_user_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"{REQUEST_PREFIX}:{kind}:reject:{user['user_id']}:{target_user_id}"),
    ]])

    await context.bot.send_message(target_user_id, prompt, parse_mode="HTML", reply_markup=keyboard)
    await update.message.reply_text(f"✅ {kind.title()} request sent to {target_name}.")


async def marry_request_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    family = db.get_family(user["user_id"]) or {}
    if family.get("partner"):
        return await update.message.reply_text("❌ You are already married.")
    await _request_with_buttons(update, context, "marry", f"💍 <b>{get_display_name(user)}</b> sent you a marriage proposal.")


async def adopt_request_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _request_with_buttons(update, context, "adopt", "👶 You received an adoption request.")


async def friend_request_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _request_with_buttons(update, context, "friend", "👥 You received a friend request.")


async def requests_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, kind, action, requester_str, target_str = q.data.split(":")
    requester_id = int(requester_str)
    target_id = int(target_str)

    if q.from_user.id != target_id:
        return await q.answer("Not your request.", show_alert=True)

    if action == "reject":
        await q.edit_message_text(f"❌ {kind.title()} request rejected.")
        return

    if kind == "marry":
        requester_family = db.get_family(requester_id) or {}
        target_family = db.get_family(target_id) or {}
        if requester_family.get("partner") or target_family.get("partner"):
            return await q.edit_message_text("❌ One of you is already married.")
        db.add_partner(requester_id, target_id)
        db.update_user(requester_id, {"status": "married"})
        db.update_user(target_id, {"status": "married"})
    elif kind == "adopt":
        requester_family = db.get_family(requester_id) or {}
        target_family = db.get_family(target_id) or {}
        if target_family.get("parents"):
            return await q.edit_message_text("❌ You already have parent records.")
        if target_id in requester_family.get("parents", []):
            return await q.edit_message_text("❌ Circular family relation blocked.")
        db.add_child(requester_id, target_id)
    elif kind == "friend":
        db.add_friend(requester_id, target_id)

    await q.edit_message_text(f"✅ {kind.title()} request accepted.")


async def siblings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    sibling_ids = db.get_siblings(user["user_id"])
    if not sibling_ids:
        return await update.message.reply_text("No siblings found.")
    names = []
    for sid in sibling_ids:
        su = db.get_user(sid)
        if su:
            names.append(get_display_name(su))
    await update.message.reply_text("🤝 <b>Siblings</b>\n" + "\n".join(f"• {n}" for n in names), parse_mode="HTML")


async def friends_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    fr = db.get_friends(user["user_id"]) or {}
    ids = fr.get("friends", [])
    if not ids:
        return await update.message.reply_text("You have no friends yet.")
    lines = []
    for fid in ids[:50]:
        fuser = db.get_user(fid)
        if fuser:
            lines.append(f"• {get_display_name(fuser)}")
    await update.message.reply_text("👥 <b>Your Friends</b>\n" + "\n".join(lines), parse_mode="HTML")


async def remove_friend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    target_user_id, _, error = await get_target_user(update, context)
    if error:
        return await update.message.reply_text(f"❌ {error}")
    db.remove_friend(user["user_id"], target_user_id)
    await update.message.reply_text("✅ Friend removed.")


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if user:
        await update.message.reply_text(f"💰 Balance: {user.get('money', 0):,} coins")


async def water_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    db.add_xp(user["user_id"], 5)
    await update.message.reply_text("💧 Plants watered! Your next harvest reward is boosted.")


async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    if not context.args:
        return await update.message.reply_text("Usage: /bet amount")
    try:
        amount = max(1, int(context.args[0]))
    except ValueError:
        return await update.message.reply_text("❌ Invalid amount.")
    if user.get("money", 0) < amount:
        return await update.message.reply_text("❌ Not enough money.")
    remaining = db.get_cooldown_remaining(user["user_id"], "bet")
    if remaining:
        return await update.message.reply_text(f"⏳ Cooldown: {remaining}s")
    win = random.choice([True, False])
    db.withdraw_money(user["user_id"], amount)
    if win:
        prize = amount * 2
        db.add_money(user["user_id"], prize)
        db.set_cooldown(user["user_id"], "bet", 15)
        return await update.message.reply_text(f"✅ You won! +{prize:,} coins")
    db.set_cooldown(user["user_id"], "bet", 15)
    await update.message.reply_text(f"❌ You lost {amount:,} coins")


async def rps_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await _ensure_registered(update)
    if not user:
        return
    options = ["rock", "paper", "scissors"]
    if not context.args or context.args[0].lower() not in options:
        return await update.message.reply_text("Usage: /rps rock|paper|scissors")
    remaining = db.get_cooldown_remaining(user["user_id"], "rps")
    if remaining:
        return await update.message.reply_text(f"⏳ Cooldown: {remaining}s")
    pick = context.args[0].lower()
    bot_pick = random.choice(options)
    wins = {("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")}
    if pick == bot_pick:
        result = "Draw"
    elif (pick, bot_pick) in wins:
        db.add_money(user["user_id"], 25)
        result = "You win! +25 coins"
    else:
        result = "You lose"
    db.set_cooldown(user["user_id"], "rps", 10)
    await update.message.reply_text(f"You: {pick}\nBot: {bot_pick}\n{result}")


async def top_garden_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = list(db.db.gardens.find().sort("total_harvested", -1).limit(10))
    text = "🌱 <b>Top Garden</b>\n"
    for i, row in enumerate(rows, 1):
        u = db.get_user(row["user_id"])
        text += f"{i}. {get_display_name(u) if u else row['user_id']} - {row.get('total_harvested', 0)}\n"
    await update.message.reply_text(text, parse_mode="HTML")


async def top_games_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = list(db.db.users.find().sort("total_commands", -1).limit(10))
    text = "🎮 <b>Top Games</b>\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. {get_display_name(row)} - {row.get('total_commands', 0)} actions\n"
    await update.message.reply_text(text, parse_mode="HTML")


async def top_money_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db.get_leaderboard("money", 10)
    text = "💰 <b>Top Money</b>\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. {get_display_name(row)} - {row.get('money', 0):,}\n"
    await update.message.reply_text(text, parse_mode="HTML")


async def top_family_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db.get_family_leaderboard(10)
    text = "👨‍👩‍👧‍👦 <b>Top Family</b>\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. {get_display_name(row)} - {row.get('children_count', 0)} children\n"
    await update.message.reply_text(text, parse_mode="HTML")


async def group_enable_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_group(update.effective_chat):
        return await update.message.reply_text("This command is for groups only.")
    member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if member.status not in ("administrator", "creator"):
        return await update.message.reply_text("❌ Admin only command.")
    db.set_group_enabled(update.effective_chat.id, True)
    await update.message.reply_text("✅ Bot enabled in this group.")


async def group_disable_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_group(update.effective_chat):
        return await update.message.reply_text("This command is for groups only.")
    member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if member.status not in ("administrator", "creator"):
        return await update.message.reply_text("❌ Admin only command.")
    db.set_group_enabled(update.effective_chat.id, False)
    await update.message.reply_text("🛑 Bot disabled in this group.")


async def group_reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_group(update.effective_chat):
        return await update.message.reply_text("This command is for groups only.")
    member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if member.status not in ("administrator", "creator"):
        return await update.message.reply_text("❌ Admin only command.")
    db.db.group_settings.delete_one({"chat_id": update.effective_chat.id})
    await update.message.reply_text("♻️ Group settings reset.")


async def backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    file_path = backup_dir / f"backup_{update.effective_user.id}.json"
    result = db.export_backup(str(file_path))
    if not result:
        return await update.message.reply_text("❌ Backup failed.")
    await update.message.reply_document(document=str(file_path), caption="✅ Backup created.")


async def restore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /restore backups/backup_file.json")
    target = Path(context.args[0])
    if not target.exists():
        return await update.message.reply_text("❌ Backup file not found on server.")
    if db.restore_backup(str(target)):
        return await update.message.reply_text("✅ Restore completed.")
    await update.message.reply_text("❌ Restore failed.")


masterplus_handlers = [
    CommandHandler("menu", menu_command),
    CommandHandler("setcommands", set_commands_command),
    CommandHandler("me", me_command),
    CommandHandler("profile", profile_lookup_command),
    CommandHandler("marry", marry_request_command),
    CommandHandler("adopt", adopt_request_command),
    CommandHandler("friend", friend_request_command),
    CommandHandler("siblings", siblings_command),
    CommandHandler("friends", friends_list_command),
    CommandHandler("removefriend", remove_friend_command),
    CommandHandler("balance", balance_command),
    CommandHandler("water", water_command),
    CommandHandler("bet", bet_command),
    CommandHandler("rps", rps_command),
    CommandHandler("topmoney", top_money_command),
    CommandHandler("topfamily", top_family_command),
    CommandHandler("topgarden", top_garden_command),
    CommandHandler("topgames", top_games_command),
    CommandHandler("enable", group_enable_command),
    CommandHandler("disable", group_disable_command),
    CommandHandler("reset", group_reset_command),
    CommandHandler("backup", backup_command),
    CommandHandler("restore", restore_command),
]

requests_callback_handler = CallbackQueryHandler(requests_callback, pattern=r"^req:(marry|adopt|friend):(accept|reject):\d+:\d+$")
