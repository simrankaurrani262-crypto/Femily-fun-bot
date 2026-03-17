"""
/tree and /fulltree command handlers
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from modules.utils.tree_generator import generate_family_tree, get_family_stats
from database import db
import io
import logging

logger = logging.getLogger(__name__)

async def tree_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate and send family tree image"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    # Show that we're generating
    await update.message.chat.send_action("upload_photo")
    
    # Generate tree image
    img = generate_family_tree(user_id)
    
    if not img:
        await update.message.reply_text("❌ Failed to generate family tree. Your family might be empty.")
        return
    
    # Convert to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    # Get family stats
    stats = get_family_stats(user_id)
    
    caption = f"""
<b>👨‍👩‍👧‍👦 Family Tree</b>

<b>Family Members:</b> {stats['total_family_members']}
<b>Partner:</b> {"✅" if stats['partner'] else "❌"}
<b>Children:</b> {stats['children_count']}
<b>Parents:</b> {stats['parents_count']}
<b>Grandparents:</b> {stats['grandparents_count']}
<b>Grandchildren:</b> {stats['grandchildren_count']}
"""
    
    await update.message.reply_photo(photo=buf, caption=caption, parse_mode="HTML")
    logger.info(f"Tree generated for {user_id}")

async def fulltree_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate full family tree with all relatives"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please use /start to register first")
        return
    
    family = db.get_family(user_id)
    
    full_tree_text = f"""
<b>👨‍👩‍👧‍👦 COMPLETE FAMILY TREE</b>

"""
    
    # Grandparents
    if family.get('grandparents'):
        full_tree_text += "<b>🧓 Grandparents:</b>\n"
        for gp_id in family['grandparents']:
            gp = db.get_user(gp_id)
            if gp:
                full_tree_text += f"  • @{gp['username']}\n"
    
    # Parents
    if family.get('parents'):
        full_tree_text += "\n<b>👪 Parents:</b>\n"
        for p_id in family['parents']:
            p = db.get_user(p_id)
            if p:
                full_tree_text += f"  • @{p['username']}\n"
    
    # You
    full_tree_text += f"\n<b>🧑 You:</b> @{user['username']}\n"
    
    # Partner
    if family.get('partner'):
        partner = db.get_user(family['partner'])
        if partner:
            full_tree_text += f"\n<b>❤️ Partner:</b> @{partner['username']}\n"
    
    # Children
    if family.get('children'):
        full_tree_text += "\n<b>👶 Children:</b>\n"
        for c_id in family['children']:
            c = db.get_user(c_id)
            if c:
                full_tree_text += f"  • @{c['username']}\n"
    
    # Grandchildren
    if family.get('grandchildren'):
        full_tree_text += "\n<b>👦 Grandchildren:</b>\n"
        for gc_id in family['grandchildren']:
            gc = db.get_user(gc_id)
            if gc:
                full_tree_text += f"  • @{gc['username']}\n"
    
    await update.message.reply_text(full_tree_text, parse_mode="HTML")
    logger.info(f"Full tree viewed by {user_id}")

tree_handler = CommandHandler('tree', tree_command)
fulltree_handler = CommandHandler('fulltree', fulltree_command)