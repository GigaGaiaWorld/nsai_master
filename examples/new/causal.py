from langda import langda_solve

model = """% ========== 多时间线推理 ========== %
0.7::burglary.
langda(LLM:"Is there heavy rain?",LOT:"search").

langda(LLM:"Repairman: '/* Repairman */'",FUP:"false").
0.8::p_alarm2.

alarm :- langda(LLM:"If there's heavy rain or burglary, alarm 1 sound an alarm").
alarm :- 
"""
ext = {"Repairman":"The probablilty of alarm 1 sound an alarm is 0.9"}
result = langda_solve('double_dc',model,'deepseek-chat', langda_ext=ext)

print(result)