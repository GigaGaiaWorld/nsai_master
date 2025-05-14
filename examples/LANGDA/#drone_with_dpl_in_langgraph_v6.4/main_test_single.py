from agent import Langda_Agent
import os
from config import paths

if __name__ == "__main__":
    def process_all_prompt_files(directory_path, model_name, addition_input):  
        # Find all files ending with "prompt.pl"
        prompt_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                prompt_files.append(os.path.join(root, file))
        print("prompt_files",prompt_files)
        # Process each prompt file
        for prompt_file in prompt_files:
            print(f"#=================Processing file: {prompt_file} =================#")

            # Extract prefix from filename (remove _prompt.pl suffix)
            file_basename = os.path.basename(prompt_file)
            prefix = file_basename.replace("_prompt.pl", "")

            # Update the prefix in addition_input
            file_specific_input = addition_input.copy()
            file_specific_input["prefix"] = prefix

            # Read the rules from the file
            with open(prompt_file, "r") as f:
                rules_string = f.read()

            # Create and run the agent
            agent = Langda_Agent(rules_string, "", model_name, addition_input=file_specific_input)
            agent.call_langda_workflow()

            print(f"#=================Completed processing: {prompt_file} =================#")

    def combine_results(directory_path):
        print("in combine_results")
        # Find all files ending with "result.txt"
        result_files = []  # Changed variable name from prompt_files to result_files
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith("result.txt"):
                    result_files.append(os.path.join(root, file))
        # Process each result file
        for result_file in result_files:  # Changed variable name from prompt_file to result_file
            file_basename = os.path.basename(result_file)

            with open(result_file, "r") as f:  # Changed from prompt_file to result_file
                result = f.read()

            with open(f"{directory_path}/gathered_final_result.txt", "a") as f:
                f.write(f"\n\n=============={file_basename}:==============\n")
                f.write(result)

    addition = {
        "prefix": "",  # Will be updated for each file
        "langda_ext": "msg_from_bot",  # Will be updated for each file
        "error_report": "",
        "config": {"configurable": {"thread_id": "42"}},
        "user_context": ""
    }
    test_path = paths.get_abscase_path("rules/test_prompt")
    final_path = paths.get_abscase_path("history/final")
    process_all_prompt_files(test_path, "deepseek-chat", addition) 
    combine_results(final_path)