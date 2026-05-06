"""
Telegram Bot for OSINT searches
Run this on your VPS for 24/7 access
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from core.osint_functions import search_all_platforms

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token (get from @BotFather)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # NEVER commit this! Use environment variables

async def start(update: Update, context: CallbackContext):
    """Send welcome message"""
    welcome = """
🤖 *OSINT Bot*
    
I can search for people across multiple platforms.
    
*Commands:*
/start - Show this message
/search [username/phone/name] - Search all platforms
/telegram [username] - Search Telegram only
/instagram [username] - Search Instagram only
/help - Show help
    
*Examples:*
/search john_doe
/search +989121234567
/telegram @username
    """
    await update.message.reply_text(welcome, parse_mode='Markdown')

async def search_command(update: Update, context: CallbackContext):
    """Search all platforms"""
    if not context.args:
        await update.message.reply_text("❌ Please provide a username, phone, or name.\nExample: /search john_doe")
        return
    
    identifier = " ".join(context.args)
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    # Search on main platforms
    platforms = ["telegram", "instagram"]
    results = search_all_platforms(identifier, platforms, identifier_type="auto")
    
    # Format results
    response = f"🔍 *Results for:* `{identifier}`\n\n"
    
    for result in results:
        platform = result["data"].get("platform", "unknown").capitalize()
        success = "✅" if result["success"] else "❌"
        response += f"*{platform}:* {success} {result['message']}\n\n"
    
    # Add inline buttons for more actions
    keyboard = [
        [InlineKeyboardButton("📊 More Platforms", callback_data=f"more_{identifier}"),
         InlineKeyboardButton("📥 Download Instagram", callback_data=f"dl_{identifier}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(response, parse_mode='Markdown', reply_markup=reply_markup)

async def platform_specific(update: Update, context: CallbackContext, platform: str):
    """Search specific platform"""
    if not context.args:
        await update.message.reply_text(f"❌ Please provide a username.\nExample: /{platform} username")
        return
    
    identifier = " ".join(context.args)
    
    await update.message.chat.send_action(action="typing")
    
    from core.osint_functions import search_telegram, search_instagram
    
    if platform == "telegram":
        result = search_telegram(identifier, "username")
    elif platform == "instagram":
        result = search_instagram(identifier, "username")
    else:
        await update.message.reply_text("❌ Unknown platform")
        return
    
    response = f"*{platform.upper()} Search:* `{identifier}`\n\n"
    response += result["message"]
    
    if result["success"] and result["data"]:
        data = result["data"]
        if platform == "instagram" and "followers" in data:
            response += f"\n👥 *Followers:* {data['followers']}"
        if "profile_url" in data:
            response += f"\n🔗 [Open Profile]({data['profile_url']})"
    
    await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)

async def telegram_search(update: Update, context: CallbackContext):
    await platform_specific(update, context, "telegram")

async def instagram_search(update: Update, context: CallbackContext):
    await platform_specific(update, context, "instagram")

async def button_callback(update: Update, context: CallbackContext):
    """Handle inline button presses"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    identifier = data.split("_", 1)[1] if "_" in data else ""
    
    if data.startswith("more_"):
        # Search all platforms including Iranian ones
        platforms = ["telegram", "instagram", "soroush", "bale", "rubika"]
        results = search_all_platforms(identifier, platforms, identifier_type="auto")
        
        response = f"🌐 *Extended Search for:* `{identifier}`\n\n"
        for result in results:
            response += f"{result['message']}\n"
        
        await query.edit_message_text(response, parse_mode='Markdown')
    
    elif data.startswith("dl_"):
        # Download Instagram posts
        from core.osint_functions import download_instagram_posts
        result = download_instagram_posts(identifier)
        await query.edit_message_text(result["message"])

async def help_command(update: Update, context: CallbackContext):
    """Send help message"""
    help_text = """
*OSINT Bot Help*
    
I can help you find information about people online.
    
*Available Commands:*
/start - Welcome message
/search [text] - Search all platforms
/telegram [username] - Search Telegram
/instagram [username] - Search Instagram
    
*Privacy:* I only search public profiles. No login required.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("telegram", telegram_search))
    application.add_handler(CommandHandler("instagram", instagram_search))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback handler for buttons
    application.add_handler(telegram.ext.CallbackQueryHandler(button_callback))
    
    # Start bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
