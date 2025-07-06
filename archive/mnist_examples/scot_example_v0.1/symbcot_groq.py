import os
import backoff  # for exponential backoff
import groq
import logging
from retrying import retry

# from tqdm import tqdm
from typing import Tuple
import datetime as dt
script_dir = os.path.dirname(os.path.abspath(__file__))

client = groq.Client()

class Groq_Reasoning_Graph_Baseline:
    def __init__(self, context_str:str, rules_str:str, facts_str:str, queries_str:str, question_str:str,
                 model_name:str, stop_words:str, save_path:str, max_new_tokens:int, use_inline_prompt:bool):
        self.groq_api = GroqModel( model_name, stop_words, max_new_tokens)

        self.context_str = context_str
        self.rules_str = rules_str
        self.facts_str = facts_str
        self.queries_str = queries_str
        self.question_str = question_str

        self.model_name = model_name
        self.save_path = save_path
        self.max_new_tokens = max_new_tokens
        self.use_inline_prompt = use_inline_prompt
    # read prompt file
    def load__translation_prompt(self):
        if not self.use_inline_prompt:
            trans_file_path = os.path.join(script_dir, "prompts/My_prompt/translation.txt")
        else:
            trans_file_path = os.path.join(script_dir, "prompts/My_prompt/translation_inline.txt")
        syntax_file_path = os.path.join(script_dir, "prompts/My_prompt/Problog_Syntax.txt")
        with open(trans_file_path) as trans_f:
            with open(syntax_file_path) as syn_f:
                in_context_examples = trans_f.read()
                in_context_examples += '\n\n'
                in_context_examples += syn_f.read()
        print("in_context_examples:",in_context_examples)
        return in_context_examples

    # replace placeholder in prompt with actual text
    def construct_translation_prompt(self, context_str, rules_str, facts_str, queries_str, question_str, in_context_examples_trans):
        full_prompt = in_context_examples_trans
        full_prompt = full_prompt.replace('[[CONTEXT]]', context_str)
        full_prompt = full_prompt.replace('[[RULE_SET]]', rules_str)
        full_prompt = full_prompt.replace('[[FACTS]]', facts_str)
        full_prompt = full_prompt.replace('[[QUERIES]]', queries_str)
        full_prompt = full_prompt.replace('[[QUESTION]]',question_str)
        return full_prompt

    # generate response
    def reasoning_graph_generation(self) -> Tuple[str, str]:
        in_context_examples_trans = self.load__translation_prompt()    
        try:
            print("Translating...")
            whole_trans_prompt = self.construct_translation_prompt(self.context_str, self.rules_str, self.facts_str, self.queries_str, self.question_str, in_context_examples_trans)
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
                print("save_directory_thinks:",save_directory_thinks)
            with open(os.path.join(save_directory_models, f'prolog_model_{model_name_parts[0]}_{datetime_ymd}_{datetime_hms}.txt'), 'w') as f:
                f.write(response_model_with_commit)
                print("save_directory_models:",save_directory_models)

        except Exception as e:
            print(f"Error in generating response: {e}")
            raise e


@backoff.on_exception(
        backoff.expo, 
        (groq.RateLimitError, groq.APIConnectionError),
        max_time = 30,
        on_backoff=lambda details: logging.warning(
            f"Retrying due to {details['exception']} (attempt {details['tries']})"
    ))
def chat_completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)


class GroqModel:
    def __init__(self, model_name, stop_words, max_new_tokens) -> None:
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.stop_words = stop_words
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def chat_generate(self, input_string, temperature = 0.0):
        response = chat_completions_with_backoff(
                model = self.model_name,
                messages=[
                        {"role": "system", "content": "You are a helpful assistant. Make sure you carefully and fully understand the details of user's requirements before you start solving the problem."},
                        {"role": "user", "content": input_string}
                    ],
                temperature = temperature,
                top_p = 1,
                stop = self.stop_words
        )
        generated_text = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        return generated_text, finish_reason

    def generate(self, input_string, temperature = 0.0):
        print("model_name: ", self.model_name)
        if self.model_name in ['deepseek-r1-distill-llama-70b', 'gpt-3.5-turbo']:
            return self.chat_generate(input_string, temperature)
        else:
            raise Exception("Model name not recognized")