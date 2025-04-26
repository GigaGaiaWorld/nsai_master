from typing import TypedDict, List, Dict
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _find_all_blocks, 
    _replace_placeholder, 
    _parse_simple_dictonary,
    _expand_nested_list,
    invoke_agent,
)
from state import BasicState, TaskStatus
from config import paths
from database import DictDB

class GenerateNodes:

    @staticmethod
    def generate_node(state:BasicState):
        """
        Regenerate specific code blocks based on evaluation.
        """
        print("processing generate_node...")
        state["status"] = TaskStatus.GNRT
        new_iter_count = state["iter_count"] + 1

        requirement_input:List[str] = []
        targeted_codes:List[dict] = []

        requirement_input = RequirementsBuilder.build_generate_info(state["langda_reqs"],state["lann_reqs"])

        # first round
        if new_iter_count == 1:
            prompt_template = state["prompt_template"]
            # Construct the requirement part of prompt:
            prompt_type = "generate"
            input={
                "context": state["user_context"],
                "rule_set":prompt_template,
                "requirements": "\n".join(requirement_input),
            }

        elif new_iter_count > 1:

            prompt_type = "regenerate"
            prompt_template = _replace_placeholder(state["prompt_template"], state["fest_codes"], state["placeholder"])
            input={
                "context": state["user_context"],
                "rule_set": prompt_template,
                "requirements":"\n".join(state["regenerate_info"]),
            }

        else:
            raise ValueError(f"iter_count has a invalid value: {state['iter_count']}")

        generated_result = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type=prompt_type, 
            input=input, 
            config=state["config"])

        paths.save_as_file(generated_result,"result",f"gnrt_{state['iter_count']}")

        generated_codes = _find_all_blocks('code',generated_result)
        for code, langda in zip(generated_codes, state["langda_dicts"]):
            targeted_codes.append({langda["HASH"]:code})

        paths.save_as_file(targeted_codes,"codes",f"gnrt_{state['iter_count']}")
        paths.save_as_file(requirement_input,"prompt",f"requ_{state['iter_count']}")

        if generated_codes:
            return {
                "generated_codes":targeted_codes,           # [{"hash1":"code block1"}, {"hash2":"code block2"}, ...]
                "iter_count":new_iter_count,
            }
        else:
            raise ValueError("generate_node: Generated code no found...")