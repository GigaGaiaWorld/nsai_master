# agent/__init__.py
from .langda_agent import (
    LangdaAgentBase,
    LangdaAgentSingleSimple, 
    LangdaAgentDoubleSimple,
    LangdaAgentDoubleDC,
    LangdaAgentDCSimple,
    LangdaAgentSingleDC,
    LangdaAgentBaseline,
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
    # GenerateNodes:double_chain_agent, GeneralNodes
    "LangdaAgentSingleDC",

    # GenerateNodes:double_chain_agent, EvaluateNodes:double_chain_agent, GeneralNodes
    'LangdaAgentDoubleSimple',
    # GenerateNodes:simple_agent, EvaluateNodes:simple_agent, GeneralNodes
    "LangdaAgentDoubleDC",
    # GenerateNodes:double_chain_agent, EvaluateNodes:simple_agent, GeneralNodes
    "LangdaAgentDCSimple",

    # Τhe noble baseline model
    "LangdaAgentBaseline",
]
