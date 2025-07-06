import re
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from main_fullvision import Langda_Agent
from config import paths
from promis_execute import promis_execution

TOKEN = "7802169894:AAFimcnhTr0mI8MK0icoSZ0_hOeIf445Rfs"
# CHAT_ID = 6639340625  # 目标聊天 ID，可是群组、频道或个人

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def process_msg_from_bot(langda_ext:str) -> dict:
    """
    I suppose the message from telegram bot is:
    from telegram: "!Secure: content about secure..."   
        ==> inside langda file: langda(LLM:"/* Secure */")  
        ==> langda(LLM:"content about secure..")
    """
    bot_pattern = r'!(\w+):\s*(.+)'
    matches = re.findall(bot_pattern, langda_ext)
    result_dict = dict(matches)

    return result_dict

async def send_photo_async(update:Update, context:ContextTypes, photo_path:str, caption:str=""):
    chat_id = update.effective_chat.id
    try:
        logger.info(f"Trying to send picture: {photo_path}")
        with open(photo_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption or "Pic"
            )
        logger.info(f"Successfully sent picture: {photo_path}")
    except Exception as e:
        logger.error(f"Error while sending picture: {e}")
        await update.message.reply_text(f"Failed to send picture: {str(e)}")

# This function will handle forwarding messages to your local code
def forward_to_local_code(message_text, update:Update=None, context:ContextTypes.DEFAULT_TYPE=None):
    """
    This function handles sending the message content to local code.
    """
    local_promis_png = paths.get_abscase_path("history/mission_landscape.png")
    msg_dict = process_msg_from_bot(message_text)
    if msg_dict:
        update.message.reply_text("Received your command, processing...")
        addition = {
            "prefix": "telegram_bot",  # Will be updated for each file
            "langda_ext": msg_dict,  # Will be updated for each file
            "error_report": "",
            "config": {"configurable": {"thread_id": "42"}},
            "user_context": ""
        }
        promis_path = paths.get_abscase_path("rules/promis_telegram_prompt.pl")
        model_name = "deepseek-chat"
        with open(promis_path, "r") as f:
            rules_string = f.read()

        # Execute Agent:
        agent = Langda_Agent(rules_string, model_name, addition_input=addition)
        agent.call_langda_workflow()  

        with open(paths.get_abscase_path("history/final/telegram_bot_final_code.pl"), "r") as f:
            result = f.read()

        # Execute Promis:
        promis_execution(result)

        # Send Image to Telegram:
        await update.message.reply_text(f"Process finished, creating image...")
        await send_photo_async(
            update, 
            context, 
            local_promis_png, 
            caption="mission_landscape.png"
        )
        return "Image created successfully!"

    # For this simple example, we'll just return a placeholder
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Bot connected. Send messages with the prefix '!{Cmd}: ...'"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        """Use '!{Cmd}:' followed by your command to send to local code.\n
For example:
from telegram: "!Secure: content about secure..."   
    ==> inside langda file: langda(LLM:"/* Secure */")  
    ==> langda(LLM:"content about secure..")
# You could send multiple commands, just make sure to use line breaks to distinguish them.""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages."""
    message_text = update.message.text
    msg_dict = process_msg_from_bot(message_text)

    # Check if the message uses our special format
    if msg_dict:
        # Forward to local code and get response
        response = forward_to_local_code(message_text, update, context)
        await update.message.reply_text(response)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    print("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()