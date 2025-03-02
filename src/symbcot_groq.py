import json
import os
# from tqdm import tqdm
from src.utils_groq import GroqModel
from typing import Tuple
import datetime as dt

class Groq_Reasoning_Graph_Baseline:
    def __init__(self, question_str: str, item_form:str, model_name: str, stop_words: str, save_path:str, max_new_tokens: int):
        self.groq_api = GroqModel( model_name, stop_words, max_new_tokens)
        self.question_str = question_str
        self.item_form = item_form
        self.model_name = model_name
        self.save_path = save_path
        self.max_new_tokens = max_new_tokens

    # read prompt file
    def load_in_context_examples_trans(self):
        file_path = os.path.join('./src/prompts/My_prompt', 'translation.txt')
        # file_path = "#Expert_System_Design/prompts/My_prompt/translation.txt"
        with open(file_path) as f:
            in_context_examples = f.read()
        return in_context_examples

    # replace placeholder in prompt with actual text
    def construct_prompt_trans(self, item_form, question_str, in_context_examples_trans):
        full_prompt = in_context_examples_trans
        full_prompt = full_prompt.replace('[[ITEM_FORM]]', item_form)
        full_prompt = full_prompt.replace('[[QUESTION]]',question_str)
        return full_prompt

    def load_questions(self):
        with open(self.data_path) as f:
            data = json.load(f)
        return data

    # generate response
    def reasoning_graph_generation(self) -> Tuple[str, str]:
        in_context_examples_trans = self.load_in_context_examples_trans()    
        try:
            print("Translating...")
            whole_trans_prompt = self.construct_prompt_trans(self.item_form, self.question_str, in_context_examples_trans)
            response_trans, _ = self.groq_api.generate(whole_trans_prompt)
            question_str_as_prolog_commits = "\n".join(["% " + q for q in (self.question_str).split("\n")])
            # save response_trans into "think" and "model" two files:
            response_think = response_trans.split("</think>")[0]
            response_model = response_trans.split("</think>")[-1]
            response_model_with_commit = "".join([response_model, question_str_as_prolog_commits])

            # save the response to a file:
            model_name_parts = self.model_name.split("-")
            # datetime = str(dt.datetime.now()).replace(" ", "_").replace(":", "-").replace(".", "-")
            now = dt.datetime.now()
            datetime_ymd = str(now.strftime("%Y-%m-%d"))
            datetime_hms = str(now.strftime("%H:%M:%S"))
            save_directory_models = os.path.join(self.save_path, "models", datetime_ymd)
            save_directory_thinks = os.path.join(self.save_path, "thinks", datetime_ymd)
            if not os.path.exists(save_directory_models):
                os.makedirs(save_directory_models, exist_ok=True)
            if not os.path.exists(save_directory_thinks):
                os.makedirs(save_directory_thinks, exist_ok=True) 
            with open(os.path.join(save_directory_thinks, f'prolog_think_{model_name_parts[0]}_{datetime_ymd}_{datetime_hms}.txt'), 'w') as f:
                f.write(response_think)
            with open(os.path.join(save_directory_models, f'prolog_model_{model_name_parts[0]}_{datetime_ymd}_{datetime_hms}.txt'), 'w') as f:
                f.write(response_model_with_commit)
            print(f"Response saved in {self.save_path}")
        except Exception as e:
            print(f"Error in generating response: {e}")
            raise e

    def update_answer(self, sample, translation, plan, output):
        final_answer = self.post_process_c(output)
        final_choice = self.final_process(final_answer)
        dict_output = {
            'id': sample['id'],
            'question': sample['question'],
            'original_context': sample['context'],
            'context': translation,
            'plan': plan,
            'execution': output,
            'predicted_answer': final_answer, 
            'answer': sample['answer'],
            'predicted_choice': final_choice
        }
        return dict_output
