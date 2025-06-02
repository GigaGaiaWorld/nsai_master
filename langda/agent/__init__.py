# agent/__init__.py
from .langda_agent import (
    LangdaAgentBase,
    LangdaAgentSingleSimple, 
    LangdaAgentDoubleSimple,
    LangdaAgentSingleReact,
    LangdaAgentDoubleReact,
    LangdaAgentSingleDC,
    LangdaAgentDoubleDC,
)
from .state import LangdaAgentProtocol
# from .generate_nodes import GenerateNodes
# from .evaluate_nodes import EvaluateNodes
# from .general_nodes import GeneralNodes
__all__ = [
    "LangdaAgentProtocol",
    "LangdaAgentBase",

    # GenerateNodes:simple_agent, GeneralNodes
    'LangdaAgentSingleSimple',
    # GenerateNodes:react_agent, GeneralNodes
    'LangdaAgentSingleReact',
    # GenerateNodes:double_chain_agent, GeneralNodes
    "LangdaAgentSingleDC",

    # GenerateNodes:simple_agent, EvaluateNodes:simple_agent, GeneralNodes
    'LangdaAgentDoubleSimple',
    # GenerateNodes:react_agent, EvaluateNodes:react_agent, GeneralNodes
    'LangdaAgentDoubleReact',
    # GenerateNodes:double_chain_agent, EvaluateNodes:double_chain_agent, GeneralNodes
    "LangdaAgentDoubleDC",

]
