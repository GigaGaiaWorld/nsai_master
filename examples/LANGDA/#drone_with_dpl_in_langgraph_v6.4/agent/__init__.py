# agent/__init__.py
from .langda_agent import (
    LangdaAgentSingleSimple, 
    LangdaAgentFullSimple,
    LangdaAgentFullDC,
    LangdaAgentSingleDC,

)
# from .generate_nodes import GenerateNodes
# from .evaluate_nodes import EvaluateNodes
# from .general_nodes import GeneralNodes
__all__ = [
    # GenerateNodes:double_chain_agent, EvaluateNodes:double_chain_agent, GeneralNodes
    'LangdaAgentFullSimple',

    # GenerateNodes:simple_agent, GeneralNodes
    'LangdaAgentSingleSimple',

    # GenerateNodes:simple_agent, EvaluateNodes:simple_agent, GeneralNodes
    "LangdaAgentFullDC",

    # GenerateNodes:double_chain_agent, GeneralNodes
    "LangdaAgentSingleDC",
    # 'GenerateNodes',
    # 'EvaluateNodes',
    # 'GeneralNodes',
]
