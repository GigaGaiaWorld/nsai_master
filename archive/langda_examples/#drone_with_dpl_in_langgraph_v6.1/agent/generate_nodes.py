from typing import List
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _find_all_blocks, 
    _replace_placeholder, 
    invoke_agent,
    _parse_simple_dictonary,
)
from state import BasicState, TaskStatus
from config import paths

class GenerateNodes:

    @staticmethod
    def generate_node(state:BasicState):
        """
        Regenerate specific code blocks based on evaluation.
        """
        print("processing generate_node...")
        state["status"] = TaskStatus.GNRT
        new_iter_count = state["iter_count"] + 1

        requirement_input:str = []
        targeted_codes:List[dict] = []
        prompt_template = _replace_placeholder(state["prompt_template"], state["fest_codes"], state["placeholder"])

        # first round
        if new_iter_count == 1:
            requirement_input = "\n".join(RequirementsBuilder.build_generate_info(state["langda_reqs"],state["lann_reqs"]))
            prompt_type = "generate"

        elif new_iter_count > 1:
            requirement_input = "\n".join(state["regenerate_info"])
            prompt_type = "regenerate"

        else:
            raise ValueError(f"iter_count has a invalid value: {state['iter_count']}")

        input={
            "context": state["user_context"],
            "rule_set": prompt_template,
            "requirements":requirement_input,
        }

        generated_result, formatted_prompt = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type=prompt_type, 
            input=input, 
            config=state["config"])

        paths.save_as_file(formatted_prompt,"prompt",f"{state['prefix']}/formatted_{prompt_type}")
        paths.save_as_file(generated_result,"result",f"{state['prefix']}/#gnrt_{state['iter_count']}")

        generated_codes = _find_all_blocks('code',generated_result)     # [{"hash":"generated code"},{"hash":"generated code"},..]
        origin_fest_codes = state["fest_codes"]
        iter = 0
        for i, fest_item in enumerate(origin_fest_codes):
            key, value = _parse_simple_dictonary(fest_item)
            if not value:
                if key not in generated_codes[iter]:
                    raise ValueError("generate_node: key does not exist in generated_codes...")
                targeted_codes.append(generated_codes[iter])
                iter += 1

        paths.save_as_file(targeted_codes,"codes",f"{state['prefix']}/#gnrt_{state['iter_count']}")

        if generated_codes:
            return {
                "generated_codes":targeted_codes,           # [{"hash1":"code block1"}, {"hash2":"code block2"}, ...]
                "iter_count":new_iter_count,
            }
        else:
            raise ValueError("generate_node: Generated Code no found...")
        
    @staticmethod
    def _decide_next_gnrt(state:BasicState):
        print("processing _decide_next_gnrt... #current round:",state["iter_count"])
        generate_error = False
        count_need_generated = 0
        for fest_code in state["fest_codes"]:
            _, value = _parse_simple_dictonary(fest_code)
            if value == None:
                count_need_generated += 1

        # if count_need_generated != len(state["generated_codes"]):
        #     print(state["fest_codes"])
        #     print(state["generated_codes"])
        #     print("_decide_next_gnrt: the length of generated code doesn't match! Try to regenerate")
        #     generate_error = True

        if generate_error:
            state["iter_count"] -= 1
            return "generate_node"
        else:
            return "test_node"