import re
import os
import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from pathlib import Path
from langda import langda_solve
from promis_execute2 import promis_execution, set_path
PERSISTENT_MSG = {"user": None, "police":None, "ask":None}
PERSISTENT_DATA = {"user": None, "police":None, "ask":None}

### ====================== the token of chat group ====================== ###
TOKEN = "7802169894:AAFimcnhTr0mI8MK0icoSZ0_hOeIf445Rfs"
# CHAT_ID = 6639340625
### ====================== the token of chat group ====================== ###
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
save_dir = current_dir / "data"

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


def process_command(message_text):
    """
    处理命令并返回结果和后续操作信息。
    这是一个同步函数，不使用await。
    """
    global PERSISTENT_MSG
    global PERSISTENT_DATA
    msg_dict = process_msg_from_bot(message_text)
    if not msg_dict:
        return {"result": "Invalid command format. Please use !Command: message format", "actions": []}

    if "User" in msg_dict:
        PERSISTENT_MSG["user"] = msg_dict["User"]
    if "Police" in msg_dict:
        PERSISTENT_MSG["police"] = msg_dict["Police"]
    if "Ask" in msg_dict:
        PERSISTENT_MSG["ask"] = msg_dict["Ask"]

    # 创建返回值
    response = {
        "result": "",
        "actions": []  # 存储需要在异步环境中执行的操作
    }
    
    local_promis_png = save_dir / "mission_landscape.png"
    print("local_promis_png",local_promis_png)
    # 添加确认消息动作
    response["actions"].append({
        "type": "send_message",
        "message": "Received your command, processing..."
    })


    model_name = "deepseek-chat"
    promis_prompt = current_dir / "promis_normal_drone.pl"
    with open(promis_prompt, "r") as f:
        rules_string = f.read()


    if "Police" in msg_dict or "User" in msg_dict:
        # ================== refresh the coordinate ================ #
        # ===================== GET COORDINATE ===================== #
        def get_coordinate(model_name, msg_dict={"User":"","Police":""}):
            danger_rules_string = f"""
% Your model here
% Earth constant
meter_per_degree(111194.93). % R * π / 180 ≈ 111194.93 meters/degree

langda(LLM:"According to the user: /* User */, the coordinate of the user is at:
please form as: user_location(X,Y).
(X and Y are longitude and latitude)", LOT:"search with 'The geographical coordinates of ... is'").

langda(LLM:"According to the police: /* Police */, the coordinate of the special zone is at (use a dummy predicate if there's none):
please form as: special_zone_location(X,Y).
(X and Y are longitude and latitude)").

relative_offset(NorthOffset, EastOffset) :-
langda(LLM:"The location of the danger zone relative to the user, in meters, calculated based on user_location and special_zone_location above"
The conversion of longitude should take into account the influence of latitude,FUP:"false").

query(relative_offset(NorthOffset, EastOffset)).
query(user_location(North, East)).
"""
            from problog import get_evaluatable
            special_model = langda_solve("double_dc",danger_rules_string, model_name, 
                        prefix="telegram_bot", langda_ext=msg_dict)
            special_result = get_evaluatable().create_from(special_model).evaluate()
            pattern = r"(\w+)\(\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\s*\)"
            result_list = []
            for key in special_result:
                match = re.match(pattern, str(key))
                if match:
                    predicate, x, y = match.groups()
                    result_list.append((x,y))
                    print(f"predicate = {predicate}, x = {x}, y = {y}")
            (user_x,user_y),(offset_x,offset_y) = result_list
            # ===================== GET COORDINATE ===================== #
            # ===================== GET COORDINATE ===================== #
            return user_x, user_y, offset_x, offset_y

        user_x, user_y, offset_x, offset_y = get_coordinate()
        PERSISTENT_MSG["user"] = (user_x, user_y)
        PERSISTENT_MSG["police"] = (offset_x, offset_y)

        # 执行 Agent:
        logger.info("Starting call_langda_workflow")
        result = langda_solve("double_dc",rules_string, model_name, 
                              prefix="telegram_bot", langda_ext=msg_dict)
        logger.info("Finished call_langda_workflow")

        # 执行 Promis:
        logger.info("Starting promis_execution")
        successs = promis_execution(result,(offset_x, offset_y),operator_location=(user_x,user_y))
        logger.info("Finished promis_execution")

        if successs:
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



    if "Ask" in msg_dict:
        def validate_path(model_name, msg_dict={"Ask":""}):
            global PERSISTENT_DATA
            danger_rules_string = f"""

            langda(LLM:"According to the user: I just updated my flying plan: [(-230,200), (-215,195), (-200,200), (-185,190), (-170,195), (-150,195), (-130,180),(-115,175), (-100,150), (-90,125), (-80,100), (-60,80), (-40,60), (-30,40),(-20,20), (-13,13), (-7,7), (0,0)],
            please form as: fly([]).
            store all the points inside the list)", LOT:"search with 'The geographical coordinates of ... is'",FUP:"false").

            query(fly(X)).
            """
            model_name = "deepseek-chat"
            import re
            import ast

            from langda import langda_solve
            from problog import get_evaluatable
            special_model = langda_solve("double_dc",danger_rules_string, model_name, 
                        prefix="telegram_bot_fly", langda_ext={"User":"Ich bin am Innenstadtcampus der Technischen Universität Darmstadt.", "Police":"Today, the police found a bomb at (49.873094, 8.658995) coordinates. Please stay at least 50 meters away."})
            special_result = get_evaluatable().create_from(special_model).evaluate()

            key = next(iter(special_result))  # 提取唯一键

            # 用正则找出中括号部分
            match = re.search(r"fly\((\[.*\])\)", str(key))
            if match:
                list_str = match.group(1)       # 获取 "[(-230, 200), ..., (0, 0)]"
                coord_list = ast.literal_eval(list_str)  # 安全地解析为 Python 列表
                print(coord_list)
            valid_list = set_path(0,0,coord_list)

            if valid_list:
                # 添加发送完成消息动作
                response["actions"].append({
                    "type": "send_analysis_result",
                    "message": "Process finished, create analysis..."
                })
                    
                response["result"] = f"{valid_list}"


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
    ==> in LangDa source code: langda(LLM:"/* Secure */")
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