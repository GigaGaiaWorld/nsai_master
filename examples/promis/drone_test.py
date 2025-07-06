import re
import os
import logging
import ast
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from pathlib import Path
from langda import langda_solve
from promis_execute2 import promis_execution, set_path
from problog import get_evaluatable

current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
save_dir = current_dir / "data"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_coordinate(model_name, msg_dict):
    """获取坐标信息"""
    danger_rules_string = """
% Your model here
% Earth constant
meter_per_degree(111194.93). % R * π / 180 ≈ 111194.93 meters/degree

langda(LLM:"According to the user: /* User */, the coordinate of the user is at:
please form as: user_location(X,Y).
(X and Y are longitude and latitude)", LOT:"search with 'The geographical coordinates of ... is'").


langda(LLM:"According to the police: /* Police */, the coordinate of the special zone is at:
please form as: special_zone_location(X,Y).
(X and Y are longitude and latitude)",LOT:"None").

relative_offset(NorthOffset, EastOffset) :-
langda(LLM:"The location of the danger zone relative to the user, in meters, calculated based on user_location and special_zone_location above
The conversion of longitude should take into account the influence of latitude",FUP:"false").

query(relative_offset(NorthOffset, EastOffset)).
query(user_location(North, East)).
"""
    while(True):
        try:
            from problog import get_evaluatable
            special_model = langda_solve("double_dc", danger_rules_string, model_name, 
                        prefix="telegram_bot", langda_ext=msg_dict, 
                        load=False)
            print(special_model)
            special_model = special_model.strip("'")
            from problog import get_evaluatable
            special_result = get_evaluatable().create_from(special_model).evaluate()

            pattern = r"(\w+)\(\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\s*\)"
            result_list = []
            for key in special_result:
                match = re.match(pattern, str(key))
                if match:
                    predicate, x, y = match.groups()
                    result_list.append((float(x),float(y)))
                    print(f"predicate = {predicate}, x = {x}, y = {y}")
            print(result_list)
            (offset_x, offset_y), (user_x, user_y) = result_list
            with open(save_dir / "get_coordinate.txt", "w") as f:
                f.write(f"({user_x}, {user_y}), ({offset_x}, {offset_y})")
            return user_x, user_y, offset_x, offset_y
        except Exception as e:
            logger.error(f"Error in get_coordinate: {e}")
            continue



def validate_path(model_name, msg_dict):
    """验证飞行路径"""
    global PERSISTENT_DATA
    
    danger_rules_string = f"""
langda(LLM:"According to the user: /* Ask */, 
please extract the points and form as: fly([]).
store all the points inside the list").

query(fly(X)).
"""
    
    # 使用传入的msg_dict而不是硬编码
    special_model = langda_solve("single_dc", danger_rules_string, model_name, 
                prefix="telegram_bot_fly", langda_ext=msg_dict,
                load=False)
    special_model = special_model.strip("'")
    special_result = get_evaluatable().create_from(special_model).evaluate()
    
    key = next(iter(special_result))  # 提取唯一键

    # 用正则找出中括号部分
    match = re.search(r"fly\((\[.*\])\)", str(key))
    if match:
        list_str = match.group(1)       # 获取 "[(-230, 200), ..., (0, 0)]"
        coord_list = ast.literal_eval(list_str)  # 安全地解析为 Python 列表
        print(f"Parsed coordinates: {coord_list}")
        
        # 修正set_path调用，添加save_dir参数
        valid_result = set_path(0, 0, coord_list, save_dir)

        return valid_result
    else:
        logger.error("Could not extract coordinate list from result")
        return None
            



if __name__ == "__main__":

    model_name = "deepseek-chat"
    promis_prompt = current_dir / "promis_normal_drone.pl"

    with open(promis_prompt, "r") as f:
        rules_string = f.read()

    prefix = "1"
    user = "Ich bin am Innenstadtcampus der Technischen Universität Darmstadt."
    police = "Today, the police found a bomb at (49.873094, 8.658995) coordinates. Please stay at least 50 meters away."
    ask = "I just updated my flying plan: [(-230,200), (-215,195), (-200,200), (-185,190), (-170,195), (-150,195), (-130,180),(-115,175), (-100,150), (-90,125), (-80,100), (-60,80), (-40,60), (-30,40),(-20,20), (-13,13), (-7,7), (0,0)], please check if it's valid or not"

    user_x, user_y, offset_x, offset_y = get_coordinate(model_name, {"User":user,"Police":police})

    result = langda_solve("double_dc", rules_string, model_name, 
                            prefix="telegram_bot_2", langda_ext={"User":user,"Police":police},
                            load=False)

    success = promis_execution(result, (offset_x, offset_y), (user_x, user_y), city_attr=f"darmstadt_{prefix}",load_uam=False)

    valid_result = validate_path(model_name, {"Ask":ask})
