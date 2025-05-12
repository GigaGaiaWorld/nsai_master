import os
import csv
import re
import json
import base64
from agent import Langda_Agent
from config import paths

def process_all_prompt_files(test_directory_path, answer_directory_path, model_name, addition_input, output_csv_path):  
    # Create/open CSV file for writing results
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='|')
        # Write header
        csv_writer.writerow(['type_chars', 'validity', 'running_time', 'iter_count', 'final_result', 'final_report'])
        
        # Find all prompt files
        prompt_files = []
        for root, _, files in os.walk(test_directory_path):
            for file in files:
                prompt_files.append(os.path.join(root, file))
        
        # Process each prompt file
        for prompt_file in prompt_files:
            print(f"#=================Processing file: {prompt_file} =================#")

            # Extract file basename
            file_basename = os.path.basename(prompt_file)
            
            # Extract 10-character type code from filename using regex
            type_match = re.match(r'([A-Za-z0-9]{10}):', file_basename)
            if not type_match:
                print(f"Warning: Could not extract type code from {file_basename}, skipping")
                continue
            
            type_chars = type_match.group(1)
            
            # Find corresponding answer file
            answer_file = None
            for root, _, files in os.walk(answer_directory_path):
                for file in files:
                    if file.startswith(type_chars):
                        answer_file = os.path.join(root, file)
                        break
                if answer_file:
                    break
            
            if not answer_file:
                print(f"============= Warning: No matching answer file found for type code {type_chars}, skipping =============")
                continue
            
            # Read answer file for comparison (true_string)
            with open(answer_file, "r") as f:
                true_string = f.read()
            
            # Read the rules from the prompt file
            with open(prompt_file, "r") as f:
                rules_string = f.read()
            
            # Update the prefix in addition_input
            file_specific_input = addition_input.copy()
            file_specific_input["prefix"] = type_chars

            # Create and run the agent
            agent = Langda_Agent(rules_string, true_string, model_name, addition_input=file_specific_input)
            result = agent.call_langda_workflow()
            
            # Extract the fields we need from the result
            try:
                validity = result.get("validity", "N/A")
                running_time = result.get("running_time", 0)
                iter_count = result.get("iter_count", 0)
                
                # 处理多行文本 - 方法1：将换行符替换为特殊标记
                final_result_text = str(result.get("final_result", "")).replace("\n", "\\n")
                final_report = str(result.get("final_report", "")).replace("\n", "\\n")
                
                # 方法2：使用base64编码（可选）
                # final_result_text = base64.b64encode(str(result.get("final_result", "")).encode()).decode()
                # final_report = base64.b64encode(str(result.get("final_report", "")).encode()).decode()
                
                # Write to CSV
                csv_writer.writerow([type_chars, validity, running_time, iter_count, final_result_text, final_report])
                
                # 同时保存详细结果到单独的JSON文件
                detailed_result = {
                    "type_chars": type_chars,
                    "validity": validity,
                    "running_time": running_time,
                    "iter_count": iter_count,
                    "final_result": result.get("final_result", ""),
                    "final_report": result.get("final_report", "")
                }
                json_output_path = os.path.join(os.path.dirname(output_csv_path), f"{type_chars}_result.json")
                with open(json_output_path, 'w', encoding='utf-8') as json_file:
                    json.dump(detailed_result, json_file, indent=2, ensure_ascii=False)
                
            except Exception as e:
                print(f"Error processing results for {file_basename}: {str(e)}")
                # Write error row
                csv_writer.writerow([type_chars, "ERROR", 0, 0, str(e), ""])
            
            print(f"#=================Completed processing: {prompt_file} =================#")

# 另一种选择：完全使用JSON格式保存所有结果
def process_all_prompt_files_json(test_directory_path, answer_directory_path, model_name, addition_input, output_json_path):
    all_results = []
    
    # Find all prompt files
    prompt_files = []
    for root, _, files in os.walk(test_directory_path):
        for file in files:
            prompt_files.append(os.path.join(root, file))
    
    # Process each prompt file
    for prompt_file in prompt_files:
        print(f"#=================Processing file: {prompt_file} =================#")
        
        # Extract file basename
        file_basename = os.path.basename(prompt_file)
        
        # Extract 10-character type code from filename using regex
        type_match = re.match(r'([A-Za-z0-9]{10}):', file_basename)
        if not type_match:
            print(f"Warning: Could not extract type code from {file_basename}, skipping")
            continue
        
        type_chars = type_match.group(1)
        
        # Find corresponding answer file
        answer_file = None
        for root, _, files in os.walk(answer_directory_path):
            for file in files:
                if file.startswith(type_chars):
                    answer_file = os.path.join(root, file)
                    break
            if answer_file:
                break
        
        if not answer_file:
            print(f"============= Warning: No matching answer file found for type code {type_chars}, skipping =============")
            continue
        
        # Read answer file for comparison (true_string)
        with open(answer_file, "r") as f:
            true_string = f.read()
        
        # Read the rules from the prompt file
        with open(prompt_file, "r") as f:
            rules_string = f.read()
        
        # Update the prefix in addition_input
        file_specific_input = addition_input.copy()
        file_specific_input["prefix"] = type_chars

        # Create and run the agent
        agent = Langda_Agent(rules_string, true_string, model_name, addition_input=file_specific_input)
        result = agent.call_langda_workflow()
        
        # Extract and format results
        try:
            entry = {
                "type_chars": type_chars, 
                "validity": result.get("validity", "N/A"),
                "running_time": result.get("running_time", 0),
                "iter_count": result.get("iter_count", 0),
                "final_result": result.get("final_result", ""),
                "final_report": result.get("final_report", "")
            }
            all_results.append(entry)
        except Exception as e:
            print(f"Error processing results for {file_basename}: {str(e)}")
            all_results.append({
                "type_chars": type_chars,
                "error": str(e),
                "validity": "ERROR",
                "running_time": 0,
                "iter_count": 0,
                "final_result": "",
                "final_report": ""
            })
        
        print(f"#=================Completed processing: {prompt_file} =================#")
    
    # Save all results to a single JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    addition = {
        "usereact": True,
        "prefix": "",  # Will be updated for each file
        "langda_ext": "msg_from_bot",
        "error_report": "",
        "config": {"configurable": {"thread_id": "42"}},
        "user_context": ""
    }
    
    test_path = paths.get_abscase_path("rules/test_prompt")
    answer_path = paths.get_abscase_path("rules/test_answer")
    output_csv_path = paths.get_abscase_path("history/comparison_results.csv")
    output_json_path = paths.get_abscase_path("history/comparison_results.json")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    
    # 选择使用哪种方式：CSV或JSON
    # 选项1: 使用CSV (带有处理过的多行内容)
    # process_all_prompt_files(test_path, answer_path, "deepseek-chat", addition, output_csv_path)
    # print(f"CSV results saved to {output_csv_path}")
    
    # 选项2: 使用JSON (更好地处理复杂内容)
    process_all_prompt_files_json(test_path, answer_path, "deepseek-chat", addition, output_json_path)
    print(f"JSON results saved to {output_json_path}")