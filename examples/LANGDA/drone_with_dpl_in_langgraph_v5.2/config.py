import os
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

origin_data_path_rel = "data/origin"
biased_data_path_rel = "data/biased"
rules_path_rel = "rules/basic"
model_path_rel = "models"

origin_data_path = os.path.join(CURRENT_PATH,origin_data_path_rel)
biased_data_path = os.path.join(CURRENT_PATH,biased_data_path_rel)
rules_path = os.path.join(CURRENT_PATH,rules_path_rel)
model_path = os.path.join(CURRENT_PATH,model_path_rel)

GENERATED_RULE_PATH = os.path.join(CURRENT_PATH,"rules/langda_ruleset/generated_v1.pl")

MODEL_PATH = os.path.join(model_path,'model_iter_DeERes.mdl')

RESULT_TRAIN_ORIGIN = os.path.join(origin_data_path,'result_train_data.txt')                     # training_data: detect_train_data.txt detectEvent
RESULT_TEST_ORIGIN = os.path.join(origin_data_path,'result_test_data.txt')                      # test_data: detect_test_data.txt  detectEvent

HAPPEN_TRAIN_ORIGIN = os.path.join(origin_data_path,'in_train_data.txt')                      # problog_train_files: happensAt (put a list here)
HAPPEN_TEST_ORIGIN = os.path.join(origin_data_path,'in_test_data.txt')                      # problog_test_files: happensAt (put a list here)


RESULT_TRAIN_BIASED = os.path.join(biased_data_path,'result_train_data.txt')                     # training_data: detect_train_data.txt detectEvent
RESULT_TEST_BIASED = os.path.join(biased_data_path,'result_test_data.txt')                       # test_data: detect_test_data.txt  detectEvent

HAPPEN_TRAIN_BIASED = os.path.join(biased_data_path,'in_train_data.txt')                    # problog_train_files: happensAt (put a list here)
HAPPEN_TEST_BIASED = os.path.join(biased_data_path,'in_test_data.txt')                      # problog_test_files: happensAt (put a list here)


with open (os.path.join(CURRENT_PATH,"prompts/system_prompt_inline.txt"), "r") as f_f:
    SYSTEM_PROMPT_INLINE = f_f.read()
with open (os.path.join(CURRENT_PATH,"prompts/system_prompt_langda.txt"), "r") as f_f:
    SYSTEM_PROMPT_FORMAT_LANGDA = f_f.read()
with open (os.path.join(CURRENT_PATH,"prompts/system_prompt_langda_fullvision.txt"), "r") as f_f:
    SYSTEM_PROMPT_FORMAT_LANGDA_FULLVISION = f_f.read()
