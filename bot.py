import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Setup Logging to view output in Render Dashboard
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 2. Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a greeting message when the command /start is issued."""
    user_name = update.effective_user.first_name
    welcome_text = (
        f"Hello {user_name}! 👋\n\n"
        f"This bot is successfully running 24/7 as a **Render Background Worker**!\n"
        f"Send me any message, and I will echo it back to you."
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a helpful message when the command /help is issued."""
    help_text = (
        "🤖 **Available Commands:**\n"
        "/start - Start the bot and get a greeting\n"
        "/help - Show this help menu\n\n"
        "Or simply text me anything, and I'll reply!"
    )
    await update.message.reply_text(help_text)

# 3. Message Handler
async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    received_text = update.message.text
    logger.info(f"Received message: '{received_text}' from user {update.effective_user.id}")
    await update.message.reply_text(f"You said: {received_text}")

# 4. Error Handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# 5. Main Execution Block
def main() -> None:
    """Start the bot."""
    # Retrieve token from Render Environment Variables
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.critical("ERROR: TELEGRAM_TOKEN environment variable is missing! Exiting...")
        sys.exit(1)

    logger.info("Initializing Telegram Bot Application...")
    
    # Build the application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # Register error handler
    application.add_error_handler(error_handler)

    # Start the Bot using Long Polling (Perfect for Background Workers)
    logger.info("Bot is starting polling... Ready for messages.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
