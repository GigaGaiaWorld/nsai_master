import os
import json
import time
from tqdm import tqdm
from config import paths
from agent import(
    LangdaAgentProtocol,
    LangdaAgentBase,
)
def process_all_prompt_files_json(Agent:LangdaAgentBase, test_directory_path, answer_directory_path, model_name, addition_input, output_json_dir):
    all_results = []
    final_result_path = os.path.join(output_json_dir,"_final_result.json")
    
    # Find all prompt files
    prompt_files = []
    for root, _, files in os.walk(test_directory_path):
        for file in files:
            prompt_files.append(os.path.join(root, file))

    total_files = len(prompt_files)
    print(f"*** Found {total_files} files to process ***")
    pbar = tqdm(total=total_files, desc="Processing files")
    total_start_time = time.time()
    
    # Process each prompt file
    for idx, prompt_file in enumerate(prompt_files, start=1):
        if idx < 24:
            continue

        process_time = 0 
        file_basename = os.path.basename(prompt_file)
        pbar.set_description(f"*** ========= Processing {file_basename} [{idx}/{total_files}] ========= ***")
        type_chars = file_basename[:10]

        # Find corresponding answer file
        answer_file = None
        for root, _, files in os.walk(answer_directory_path):
            for file in files:
                if file.startswith(type_chars):
                    answer_file = os.path.join(root, file)
                    break
            if answer_file:
                break

        # Read answer file for comparison (true_string)
        with open(answer_file, "r") as f:
            true_string = f.read()

        # Read the rules from the prompt file
        with open(prompt_file, "r") as f:
            rules_string = f.read()

        # Update the prefix in addition_input
        file_specific_input = addition_input.copy()
        file_specific_input["prefix"] = file_basename

        # File process start time
        start_time = time.time()

        print(f"\nStarting Langda_Agent for {file_basename}...")
        agent:LangdaAgentProtocol = Agent(rules_string, true_string, model_name, addition_input=file_specific_input)
        print("Calling langda_workflow...")
        # Direct call without timeout
        result = agent.call_langda_workflow()
        print(f"Workflow completed for {file_basename}\n\n")
        # Summary of each file
        process_time = time.time() - start_time

        # Extract and format results
        entry = {
            "file_name": file_basename, 
            "Validity_form": result.get("Validity_form", "N/A"),
            "Validity_result": result.get("Validity_result", "N/A"),
            "running_time": result.get("running_time", "None"),
            "iter_count": result.get("iter_count", "None"),
            "process_time": process_time,
            "final_result": result.get("final_result", ""),
            "final_report": result.get("final_report", "")
        }
        all_results.append(entry)

        # Save a separate JSON file for viewing a single result
        json_output_path = os.path.join(output_json_dir, f"{file_basename}_result.json")
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(entry, json_file, indent=2, ensure_ascii=False)

        # Update progress bar
        pbar.update(1)
        pbar.set_postfix(validity=str(result.get("Validity_result", "N/A")), time=f"{process_time:.1f}s")

        # Save intermediate results
        with open(final_result_path + ".temp", 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

    pbar.close()

    # Total Summary
    total_process_time = time.time() - total_start_time
    summary = {
        "total_files": total_files,
        "processed_files": len(all_results),
        "total_process_time": total_process_time,
        "average_process_time": total_process_time / len(all_results) if all_results else 0,
        "valid_count": sum(1 for r in all_results if str(r.get("Validity_form")).lower() == "true"),
        "invalid_count": sum(1 for r in all_results if str(r.get("Validity_form")).lower() == "false"),
        "error_count": sum(1 for r in all_results if r.get("Validity_form") == "ERROR")
    }
    
    # Save results and summary together
    final_result = {
        "summary": summary,
        "results": all_results
    }
    # Save all results to a single JSON file
    with open(final_result_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessing Summary:")
    print(f"- Total files: {summary['total_files']}")
    print(f"- Processed: {summary['processed_files']}")
    print(f"- Valid: {summary['valid_count']}")
    print(f"- Invalid: {summary['invalid_count']}")
    print(f"- Errors: {summary['error_count']}")
    print(f"- Total time: {summary['total_process_time']:.1f}s")
    print(f"- Avg time per file: {summary['average_process_time']:.1f}s")
    
    return final_result


from agent import (
    LangdaAgentSingleSimple, 
    LangdaAgentDoubleSimple,
    LangdaAgentDoubleDC,
    LangdaAgentDCSimple,
    LangdaAgentSingleDC,
)

if __name__ == "__main__":
    addition = {
        "prefix": "",  # Will be updated for each file
        "langda_ext": "msg_from_bot",
        "error_report": "",
        "config": {"configurable": {"thread_id": "42"}},
        "user_context": ""
    }

    test_path = paths.get_abscase_path("rules/test_prompt")
    answer_path = paths.get_abscase_path("rules/test_answer")
    output_csv_path = paths.get_abscase_path("history/comparison_results.csv")
    output_json_dir = paths.get_abscase_path("history/json")
    output_json_dir.mkdir(parents=True, exist_ok=True)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_json_dir), exist_ok=True)
    
    # Main function call - without timeout parameter
    process_all_prompt_files_json(
        Agent = LangdaAgentDoubleDC,
        test_directory_path = test_path, 
        answer_directory_path = answer_path, 
        model_name = "deepseek-chat", 
        addition_input = addition, 
        output_json_dir = output_json_dir
    )
    print(f"JSON results saved to {output_json_dir}")