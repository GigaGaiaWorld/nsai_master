import re
import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from agent import (
    LangdaAgentSingleSimple, 
    LangdaAgentDoubleSimple,
    LangdaAgentDoubleDC,
    LangdaAgentDCSimple,
    LangdaAgentSingleDC,
)
from config import paths
from promis_execute import promis_execution

TOKEN = "7802169894:AAFimcnhTr0mI8MK0icoSZ0_hOeIf445Rfs"
# CHAT_ID = 6639340625

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

async def send_photo_async(update:Update, context:ContextTypes.DEFAULT_TYPE, photo_path, caption=""):
    """异步发送图片到聊天。"""
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
        return True
    except Exception as e:
        logger.error(f"Error while sending picture: {e}")
        await update.message.reply_text(f"Failed to send picture: {str(e)}")
        return False

# 修改为同步函数，但返回需要进行的后续操作
def process_command(message_text):
    """
    处理命令并返回结果和后续操作信息。
    这是一个同步函数，不使用await。
    """
    msg_dict = process_msg_from_bot(message_text)
    if not msg_dict:
        return {"result": "Invalid command format. Please use !Command: message format", "actions": []}
    
    # 创建返回值
    response = {
        "result": "",
        "actions": []  # 存储需要在异步环境中执行的操作
    }
    
    local_promis_png = paths.get_abscase_path("history/mission_landscape.png")
    
    # 添加确认消息动作
    response["actions"].append({
        "type": "send_message",
        "message": "Received your command, processing..."
    })
    
    addition = {
        "prefix": "telegram_bot",
        "langda_ext": msg_dict,
        "error_report": "",
        "config": {"configurable": {"thread_id": "42"}},
        "user_context": ""
    }
    
    try:
        promis_path = paths.get_abscase_path("rules/promis_telegram_prompt.pl")
        model_name = "deepseek-chat"
        
        with open(promis_path, "r") as f:
            rules_string = f.read()
        
        # 执行 Agent:
        logger.info("Starting call_langda_workflow")
        agent = Langda_Agent(rules_string, model_name, addition_input=addition)
        agent.call_langda_workflow()  
        logger.info("Finished call_langda_workflow")
        
        result_path = paths.get_abscase_path("history/final/telegram_bot_final_code.pl")
        
        if os.path.exists(result_path):
            with open(result_path, "r") as f:
                result = f.read()
            
            # 执行 Promis:
            logger.info("Starting promis_execution")
            promis_execution(result)
            logger.info("Finished promis_execution")
            
            # 添加发送完成消息动作
            response["actions"].append({
                "type": "send_message",
                "message": "Process finished, creating image..."
            })
            
            # 添加发送图片动作
            if os.path.exists(local_promis_png):
                response["actions"].append({
                    "type": "send_photo",
                    "path": local_promis_png,
                    "caption": "mission_landscape.png"
                })
                
                response["result"] = "Image created successfully!"
            else:
                response["result"] = "Process completed, but image file was not found."
        else:
            response["result"] = "Process completed, but result file was not found."
    
    except Exception as e:
        logger.error(f"Error while processing command: {e}", exc_info=True)
        response["result"] = f"Error while processing command: {str(e)}"
    
    return response

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

async def send_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /sendimage 命令，发送指定路径的图片。"""
    if not context.args:
        await update.message.reply_text("Please provide an image path, e.g.: /sendimage path/to/image.jpg")
        return
    
    image_path = " ".join(context.args)
    if not os.path.exists(image_path):
        await update.message.reply_text(f"Image not found: {image_path}")
        return
    
    await send_photo_async(
        update, 
        context, 
        image_path, 
        caption=f"Image: {os.path.basename(image_path)}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages."""
    message_text = update.message.text
    logger.info(f"Received message: {message_text}")
    
    msg_dict = process_msg_from_bot(message_text)

    # Check if the message uses our special format
    if msg_dict:
        # 处理特殊格式的 Image 命令
        if "Image" in msg_dict:
            image_path = msg_dict["Image"].strip()
            if not os.path.isabs(image_path):
                image_path = os.path.abspath(image_path)
                
            if os.path.exists(image_path):
                await update.message.reply_text(f"Sending image: {os.path.basename(image_path)}")
                await send_photo_async(
                    update, 
                    context, 
                    image_path, 
                    caption=f"Image: {os.path.basename(image_path)}"
                )
            else:
                await update.message.reply_text(f"Image not found: {image_path}")
            return
        
        # 处理其他命令
        # 使用同步函数处理命令，然后异步执行返回的操作
        response = process_command(message_text)
        
        # 执行返回的所有操作
        for action in response["actions"]:
            if action["type"] == "send_message":
                await update.message.reply_text(action["message"])
            elif action["type"] == "send_photo":
                await send_photo_async(update, context, action["path"], action["caption"])
        
        # 发送最终结果
        if response["result"]:
            await update.message.reply_text(response["result"])

def main() -> None:
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("sendimage", send_image_command))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Run the bot until the user presses Ctrl-C
        print("Starting bot...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()