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

SYSTEM_PROMPT_FORMAT_INLINE = """

<context>
{context}
<\context>

<facts>
### There are two different types of facts write as predicates: "happensAt" and "event". Whenever you use facts inside a rule, you should follow the following form:

1\. happensAt are always given in following forms together with rules, you should not create this part:

 happensAt(Event1, Event2, ...,Event-n, Timestamp).

 from Event1, Event2 to Event-n are different events that happens at same time Timestamp,

 for example:

 happensAt(boy, alien, 12). means there's two events(boy and alien) happens at timestamp 12.

2\. events are always given in following forms together with rules, you should not create this part:

 event<Event_name>(Event, Label).

 event predicate could follow the above form, the <Event_name> could be replaced to distinguish different events, which also means they correspond to different mapping domains,

 for example:

 event1(14243, 2). could have one of the Label1 from [0,1,2,3], means event 14243 will be classified as class 2.

 event2(dog, black). could have one of the Label2 from [black,white], means event dog will be classified as class black.
<\facts>

### Your task is to modify the following given DeepProblog rules based on the user's instructions. And generate the whole new code. 

### Below is the demand of user that you need to fullfill with your generated new code:

{requirements}

### Your code should follow the following prolog format code:
{rule_set}
\-----


# Note:

1. Make sure you capture all the information from the context in the translation.
    
2. Make sure you follow the instruction and example to translate the information.
    
3. Please ensure your answer together with current code is directly executable.
    
4. Do not generate any descriptive content. Only generate the code.

5. Let's think step by step.
"""

SYSTEM_PROMPT_FORMAT_LANGDA = """

<context>
{context}
<\context>

<facts>
### There are two different types of facts write as predicates: "happensAt" and "event". Whenever you use facts inside a rule, you should follow the following form:

1\. happensAt are always given in following forms together with rules, you should not create this part:

 happensAt(Event1, Event2, ...,Event-n, Timestamp).

 from Event1, Event2 to Event-n are different events that happens at same time Timestamp,

 for example:

 happensAt(boy, alien, 12). means there's two events(boy and alien) happens at timestamp 12.

2\. events are always given in following forms together with rules, you should not create this part:

 event<Event_name>(Event, Label).

 event predicate could follow the above form, the <Event_name> could be replaced to distinguish different events, which also means they correspond to different mapping domains,

 for example:

 event1(14243, 2). could have one of the Label1 from [0,1,2,3], means event 14243 will be classified as class 2.

 event2(dog, black). could have one of the Label2 from [black,white], means event dog will be classified as class black.
<\facts>

### Your task is to modify the following given DeepProblog rules based on the user's instructions. And generate the new codes. 

### Below are the requirements of user that you need to fullfill with your generated new code, for each requirement, you will generate a separate code block:

{requirements}


### Complete the Prolog-style rule code according to the following description. Your task is to only give the part of the code that fits the `{{LANGDA}}` placeholder, and nothing more. Please first analyze the structure and logic of the existing code, and then create additional code according to the user's instructions so that it conforms to the DeepProblog syntax. Please add necessary comments in the code to explain the function of each part.
In addition, make sure you capture all the information from the context in the translation. Please pay attention to maintain the consistency between the generated code and the original code. If you use new predicates, you need to pay attention to ensure the complete logic. Please ensure your answer together with current code is directly executable.
{rule_set}
\-----
"""