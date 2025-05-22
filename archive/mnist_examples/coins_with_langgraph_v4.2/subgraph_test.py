import os
import asyncio
from typing import List, TypedDict, Optional
from dotenv import load_dotenv
from state import BasicState, TaskStatus
load_dotenv()
from langchain.tools import BaseTool
from langgraph.prebuilt import create_react_agent, ToolNode
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import END

from tools_v1 import CustomTestTool


def print_stream(stream):
    for s in stream:
        messages = s["messages"][-1]
        print(f"Stream item type: {type(s)}")
        print(f"Stream item content: {s}")
        if "tool_calls" in s:
            print(f"Tool calls: {s['tool_calls']}")
        if "tool_results" in s:
            print(f"Tool results: {s['tool_results']}")
        
        if isinstance(messages, tuple):
            print(f"Tuple message: {messages}")
        else:
            try:
                print(f"Message content: {messages.content}")
                messages.pretty_print()
            except AttributeError:
                print(f"Cannot pretty print: {messages}")

def test_node(state:BasicState):
    state["status"] = TaskStatus.CODE_TESTING
    my_test_tool = CustomTestTool()

    TOOLS: List[BaseTool] = [
        my_test_tool,
    ]
    model = ChatDeepSeek(model="deepseek-chat", temperature=0).bind_tools(TOOLS)
    graph = create_react_agent(
        model, 
        tools=TOOLS,
    )
    # query = (
    #     "请测试当前的 Problog 模型。使用以下参数："
    #     "网络列表为 [('net1', 1), ('net2', 2)]，基础配置文件为 'examples/MNIST/coins_with_langgraph/rules/basic/DeE.pl'，"
    #     "加载模型为'examples/MNIST/coins_with_langgraph/models/model_iter_basic_detect.mdl'模型实例，并且使用biased测试数据。"
    # )
    query = (
        "please test, use biased test data, the logic model is 'coin_new_model.pl'."
    )
    print_stream(graph.stream(input={"messages": [("user",query)]}, 
                            config={"configurable": {"thread_id": "2"}},
                            stream_mode="values"))


def feedback_node(state: BasicState):
    while True:
        user_feedback = input("Are you satisfied with the results? (yes/no): ").strip().lower()

        if user_feedback in ("yes", "y"):
            state["status"] = TaskStatus.COMPLETED
            print("Great! Task marked as completed.")
            return state

        elif user_feedback in ("no", "n"):
            user_advice = input("Could you tell me the specific reason? ").strip()
            state["status"] = TaskStatus.FAILED
            state["user_feedback"] = user_advice
            print("Thanks for your feedback! Task marked as failed.")
            return state

        else:
            print("Invalid input. Please answer 'yes' or 'no'.")




