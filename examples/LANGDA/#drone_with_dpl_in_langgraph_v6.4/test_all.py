import os
import json
import csv
import re
from pathlib import Path
from agent import Langda_Agent

def extract_type_code(filename):
    """Extract the 10-character type code from the filename."""
    # For test_prompt files: {10-char-type}:{rest-of-filename}
    # For test_answer files: {10-char-type}
    
    parts = filename.split(':')
    if len(parts) > 1:  # test_prompt format
        return parts[0]
    else:  # test_answer format or other
        # Just take the first 10 characters as the type code
        return filename[:10]

def process_files(test_prompt_dir, test_answer_dir, output_csv):
    """
    Process files from test_prompt and test_answer directories,
    compare them, and write results to a CSV file.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    # Get all prompt files ending with "prompt.pl"
    prompt_files = []
    for root, _, files in os.walk(test_prompt_dir):
        for file in files:
            if file.endswith("prompt.pl"):
                prompt_files.append(os.path.join(root, file))
    
    # Write header to CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow(['type_code', 'validity', 'running_time', 'iter_count', 'final_result', 'final_report'])
    
    # Process each prompt file
    for prompt_file_path in prompt_files:
        prompt_filename = os.path.basename(prompt_file_path)
        
        # Extract type code
        type_code = extract_type_code(prompt_filename.replace("_prompt.pl", ""))
        
        # Look for corresponding result file in the history/final directory
        # The result filename pattern needs to be determined based on your system
        result_filename = f"{type_code}_result.txt"
        result_path = os.path.join(os.path.dirname(output_csv), "history", "final", result_filename)
        
        # Check if the result file exists
        if not os.path.exists(result_path):
            print(f"Warning: Result file {result_path} not found for prompt {prompt_filename}")
            continue
        
        # Read the result file
        with open(result_path, 'r') as f:
            result_content = f.read()
        
        # Extract JSON content using regex
        json_match = re.search(r'"final_result":\s*({.*})', result_content, re.DOTALL)
        if not json_match:
            print(f"Warning: Could not find final_result JSON in {result_path}")
            continue
        
        try:
            # Extract and parse the JSON
            json_str = json_match.group(1)
            # Handle potential nested JSON issues
            json_str = json_str.strip()
            if json_str.endswith(','):
                json_str = json_str[:-1]
            
            # Try to parse the JSON structure
            result_data = json.loads("{" + f'"final_result":{json_str}' + "}")
            
            # Extract required fields
            validity = result_data['final_result'].get('validity', '')
            running_time = result_data['final_result'].get('running_time', '')
            iter_count = result_data['final_result'].get('iter_count', '')
            final_result = result_data['final_result'].get('final_result', '')
            final_report = result_data['final_result'].get('final_report', '')
            
            # Write to CSV
            with open(output_csv, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter='|')
                csvwriter.writerow([type_code, validity, running_time, iter_count, final_result, final_report])
                
            print(f"Processed {prompt_filename} successfully.")
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {result_path}: {e}")
            continue
        except KeyError as e:
            print(f"Missing key in JSON from {result_path}: {e}")
            continue

if __name__ == "__main__":
    from config import paths
    
    test_prompt_dir = paths.get_abscase_path("rules/test_prompt")
    test_answer_dir = paths.get_abscase_path("rules/test_answer")
    output_csv = paths.get_abscase_path("results/comparison_results.csv")
    
    process_files(test_prompt_dir, test_answer_dir, output_csv)
    print(f"Results written to {output_csv}")