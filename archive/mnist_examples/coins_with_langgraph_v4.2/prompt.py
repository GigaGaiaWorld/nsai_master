
import os
from typing import List, Optional
dir_path = os.path.dirname(os.path.abspath(__file__))

SYSTEM_PROMPT_FORMAT = """

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

### Your task is to modify the following given DeepProblog rules based on the user's instructions. And generate the whole new code. Please first analyze the structure and logic of the existing code, and then create additional code according to the user's instructions so that it conforms to the DeepProblog syntax. Please add necessary comments in the code to explain the function of each part.

### Below is the demand of user that you need to fullfill with your generated new code:

{requirements}

And the target predicate to express your results should be in form of {result}
\-----


### The generated new code should based on the code below:

{rule_set}
\-----


# Note:

1. Make sure you capture all the information from the context in the translation.
    
2. Make sure you follow the instruction and example to translate the information.
    
3. Please ensure your answer together with current code is directly executable.
    
4. Do not generate any descriptive content. Only generate the code.

5. Let's think step by step.
"""

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
# prompt = ChatPromptTemplate.from_messages([
#         SystemMessage("You are a helpful assistant that helps the user to generate deepproblog code."),
#         MessagesPlaceholder(variable_name="conversation"),
#         HumanMessagePromptTemplate.from_template(SYSTEM_PROMPT_FORMAT),
# ])
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
    ("human", SYSTEM_PROMPT_FORMAT)
])

def construct_prompt(context:str, requirements:str):
    """
    Construct the complete prompt for LLM

    Parameters:
        context (str): context informations
        requirements (str): requirements of the user
        conversation (List[tuple], optional): the history of conversation, empty list as default

    Returns:
        dict: a dictionary
    """
    if conversation is None:
        conversation = []

    rule_set_path = os.path.join(dir_path,"rules/basic/DeE.pl")
    with open(rule_set_path) as f:
        logic_string = f.read()

    formatted_prompt = prompt.invoke(
        input={
            "context": context,
            "requirements": requirements,
            "result": "result(win=X, T)",
            "rule_set":logic_string,
        }
    )
    return formatted_prompt


if __name__ == '__main__':
    prompt = construct_prompt("assssssss","nononononnonono",None)

    import pprint as pp
    pp.pp(prompt)