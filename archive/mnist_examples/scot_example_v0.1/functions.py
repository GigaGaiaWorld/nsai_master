from problog.program import PrologString
from problog import get_evaluatable
import os# define the arguments for the model:

def get_model_files(date:str, model_name:str):
    model_files = []
    for root, dirs, files in os.walk(os.path.join("src/generated/models", date)):
        for file in files:
            if file.startswith("prolog_model_"+model_name+"_"):
                model_files.append(os.path.join(root, file))

    models_string_dir = {}
    for file in model_files:
        with open(file, 'r') as f:
            models_string_dir[file] = f.read()
    print(f"Found {len(models_string_dir)}")
    return models_string_dir

def get_single_model_file_with_path(model_path:str):

    if os.path.isfile(model_path):
        with open(model_path, 'r') as f:
            model_string = f.read()
    else:
        print(f"this file could not be found")
    return model_string

def prolog_reasoning(model:str):
    result = get_evaluatable().create_from(PrologString(model)).evaluate()
    print("% ProbLog Inference Result：")
    for query_key, probability in result.items():
        print(f"{query_key} = {probability:.4f}")