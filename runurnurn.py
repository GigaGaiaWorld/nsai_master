# runurnurn.py
from langda import langda_solve
# 先导入运行时模块（注册外部谓词）

# 注意：先调用langda_pred来注入代码
# langda_pred("HASH1234")

# 然后再执行查询
model = """
# Try langda solve:
operation(X,Y,Z) :-
    langda(LLM:"exact: ").

query(operation(3,4,X)).
"""
langda_solve("double_dc",model)