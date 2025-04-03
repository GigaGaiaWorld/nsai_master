import os
origin_data_path = "data/origin"
biased_data_path = "data/biased"
rules_path = "rules/basic"
model_path = "models"

LOGIC_ORIGIN = [
    # os.path.join(model_path,"event_occ_defs.pl"),                  # problog_files: ruleset,
    os.path.join(rules_path,"DeE_ResDeE_rmNet.pl"),          # problog_files: ruleset,
]

LOGIC_COMPLEX = [
    os.path.join(rules_path,"rules/llm_gen/coin_new_model.pl"),          # problog_files: ruleset,
]

RESULT_TRAIN_ORIGIN = os.path.join(origin_data_path,'result_train_data.txt')                     # training_data: detect_train_data.txt detectEvent
RESULT_TEST_ORIGIN = os.path.join(origin_data_path,'result_test_data.txt')                      # test_data: detect_test_data.txt  detectEvent

HAPPEN_TRAIN_ORIGIN = os.path.join(origin_data_path,'in_train_data.txt')                      # problog_train_files: happensAt (put a list here)
HAPPEN_TEST_ORIGIN = os.path.join(origin_data_path,'in_test_data.txt')                      # problog_test_files: happensAt (put a list here)


RESULT_TRAIN_BIASED = os.path.join(biased_data_path,'result_train_data.txt')                     # training_data: detect_train_data.txt detectEvent
RESULT_TEST_BIASED = os.path.join(biased_data_path,'result_test_data.txt')                       # test_data: detect_test_data.txt  detectEvent

HAPPEN_TRAIN_BIASED = os.path.join(biased_data_path,'in_train_data.txt')                    # problog_train_files: happensAt (put a list here)
HAPPEN_TEST_BIASED = os.path.join(biased_data_path,'in_test_data.txt')                      # problog_test_files: happensAt (put a list here)
