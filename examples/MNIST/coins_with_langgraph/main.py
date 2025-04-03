# 示例：langgraph_hello.py
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage

# pip install langgraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState # 导入状态图和状态:
from subgraph_test import test_node, feedback_node
from state import BasicState, TaskStatus

from dotenv import load_dotenv
load_dotenv()

def decide_next(state:BasicState):
    if state["status"] == TaskStatus.COMPLETED:
        return END
    elif state["status"] == TaskStatus.FAILED:
        return "test_node"

state = BasicState()
test_build = StateGraph(MessagesState)

test_build.add_node("test_node", test_node)
test_build.add_node("feedback_node", feedback_node)

# 4. 定义入口点和图边
# 设置入口点为"agent"
# 这意味着这是第一个被调用的节点
test_build.set_entry_point("test_node")

# 添加条件边
test_build.add_conditional_edges(
    "feedback_node",
    decide_next,
)


test_build.add_edge(start_key="test_node", end_key='feedback_node')

checkpointer = MemorySaver()


test_subgraph = test_build.compile(checkpointer=checkpointer)

test_subgraph.invoke(
    input={"iter_count": 0},
    config={"configurable": {"thread_id": 42}}
)

import os
curr_dir = os.path.dirname(os.path.abspath(__file__))
graph_png = test_subgraph.get_graph().draw_mermaid_png()
with open(os.path.join(curr_dir,"subgraph_test.png"), "wb") as f:
    f.write(graph_png)


