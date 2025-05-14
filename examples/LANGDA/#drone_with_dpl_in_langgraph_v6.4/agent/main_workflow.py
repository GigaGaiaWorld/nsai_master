# import time

# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import StateGraph

# from state import BasicState
# from utils import _draw_mermaid_png
# from agent.generate_nodes import GenerateNodes
# from agent.evaluate_nodes import EvaluateNodes
# from agent.general_nodes import GeneralNodes

# """ 
# Full vision means that LLM processes the complete prompt uniformly and generates all code content at the same time.
# """
# class Langda_Agent(object):
#     def __init__(self, 
#                 rule_string:str, # the input test rule string
#                 true_string:str, # the complete answer rule string(just for testing)
#                 model_name, 
#                 addition_input:dict={
#                      "prefix":"",
#                      "langda_ext":"",
#                      "user_context":"",
#                      "error_report":"",
#                      "config":{"configurable": {"thread_id": "42"}}
#                 },
#                 caching:bool=False, saving:bool=False):

#         # User inputs:
#         self.state = BasicState()
#         self.state["config"] = addition_input["config"]
#         self.state["prefix"] = addition_input["prefix"]
#         self.state["langda_ext"] = addition_input["langda_ext"]
#         self.state["model_name"] = model_name
#         self.state["rule_string"] = rule_string
#         self.state["true_string"] = true_string
#         self.state["user_context"] = addition_input["user_context"]

#         # Prompting static parameters:
#         self.state["tools"] = [
#             "search_tool",
#             "Prolog_builtins_retriever_tool",
#             "finish_tool",
#             ]

#         self.state["placeholder"] = "{{LANGDA}}"
#         self.state["error_report"] = addition_input["error_report"]

#         self.checkpointer = MemorySaver()

#     def call_langda_workflow(self) -> dict:
#         self.state["srttime"] = time.time()
#         self.state["iter_count"] = 0

#         langda_workflow = StateGraph(BasicState)
#         langda_workflow.set_entry_point("init_node")
#         langda_workflow.add_node("init_node", GeneralNodes.init_node)
#         langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
#         langda_workflow.add_node("test_node", EvaluateNodes.test_node)
#         langda_workflow.add_node("summary_node", GeneralNodes.summary_node)

#         langda_workflow.add_conditional_edges("init_node",GeneralNodes._decide_next_init, 
#             {
#                 "generate_node": "generate_node",
#                 "summary_node": "summary_node"
#             })
#         langda_workflow.add_conditional_edges("generate_node",GenerateNodes._decide_next_gnrt, 
#             {
#                 "generate_node": "generate_node",
#                 "test_node": "test_node"
#             })
#         langda_workflow.add_conditional_edges("test_node",EvaluateNodes._decide_next_eval, 
#             {
#                 "generate_node": "generate_node",
#                 "summary_node": "summary_node"
#             })
#         langda_workflow.set_finish_point("summary_node")

#         langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
#         self.state = langda_agent.invoke(self.state, config=self.state["config"])

#         _draw_mermaid_png(langda_agent, "langda_agent")

#         return self.state["final_result"]
