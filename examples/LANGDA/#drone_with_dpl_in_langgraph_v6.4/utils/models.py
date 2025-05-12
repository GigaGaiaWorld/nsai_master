from typing import Literal, Dict, List, Tuple
from pydantic import BaseModel, Field

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

import re
from utils.format_tools import (
    _replace_placeholder, 
)
from langchain.tools import BaseTool
from langchain.schema import BaseOutputParser
from langchain.schema.runnable import Runnable
from langchain.chat_models.base import BaseChatModel
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.agents import (
    create_react_agent,
    create_tool_calling_agent,
    AgentExecutor,
)
from config import paths
paths.load_my_env()

class NoOpOutputParser(BaseOutputParser[str]):
    def parse(self, text: str) -> str:
        return text

    def get_format_instructions(self) -> str:
        return ""

class LLMConfig(BaseModel):
    model: str
    api_key: str
    api_typ: str
    api_ver: str
    temperature: float = 0.0

class AgentSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="gnrt_",
        env_nested_delimiter="_",
        env_nested_max_split = 1,
        extra="ignore"
    )
    deepseek: LLMConfig # 1. subconfig：DeepSeek
    openai: LLMConfig   # 2. subconfig：OpenAI # I have no api key... 
    groq: LLMConfig     # 3. subconfig：GroqCloud

class LangdaAgentExecutor(BaseModel):
    """
    when creating, you should give the model_name and tools
    invoke_react_agent: reactive agent
    invoke_agent:       regular agent
    """
    cfgs: AgentSettings = Field(default_factory=AgentSettings)    
    tools: List[BaseTool]
    model_name:str
    # File name configurations:
    prompt_names: Dict[str, str] = Field(default={
        "generate": "system_generate_prompt_fullvision.txt",
        "evaluate": "system_evaluate_prompt_fullvision.txt",
        "regenerate": "system_regenerate_prompt_fullvision.txt",
        "final_test": "system_final_test_prompt_fullvision.txt",
    })
    react_prompt_names: Dict[str, str] = Field(default={
        "generate": "system_generate_prompt_fullvision_react.txt",
        "evaluate": "system_evaluate_prompt_fullvision_react.txt",
        "regenerate": "system_regenerate_prompt_fullvision_react.txt",
        "final_test": "system_final_test_prompt_fullvision_react.txt",
    })


    def get_prompt_path(self, prompt_name: str, usereact:bool) -> Path:
        """
        Get path for prompt files.
        Args:
            prompt_name: One of ["evaluate", "generate", "regenerate"]
        """
        if not usereact:
            if prompt_name not in self.prompt_names:
                raise FileExistsError(f"Unknown prompt: {prompt_name}.")
            return paths._get_path("prompts", self.prompt_names[prompt_name])
        else:
            if prompt_name not in self.react_prompt_names:
                raise FileExistsError(f"Unknown prompt: {prompt_name}.")
            return paths._get_path("prompts", self.react_prompt_names[prompt_name])
    
    def load_prompt(self, prompt: Literal["evaluate", "generate", "regenerate", "final_test"], usereact:bool) -> str:
        """
        Load prompt content from file.
        Args:
            prompt: One of ["evaluate", "generate", "regenerate", "final_test"]
            usereact: use react prompt or not
        """
        path = self.get_prompt_path(prompt, usereact)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            raise FileExistsError(f"Prompt file not found: {path}")

    def get_model(self) -> BaseChatModel:
        model_factories = {
            "gpt": lambda: ChatOpenAI(
                model_name=self.cfgs.openai.model,
                temperature=self.cfgs.openai.temperature,
                openai_api_key=self.cfgs.openai.api_key,
            ),
            "deepseek": lambda: ChatDeepSeek(
                model=self.cfgs.deepseek.model,
                temperature=self.cfgs.deepseek.temperature,
                api_key=self.cfgs.deepseek.api_key,
            ),
            "groq": lambda: ChatGroq(
                model=self.cfgs.groq.model,
                temperature=self.cfgs.groq.temperature,
                api_key=self.cfgs.groq.api_key,
            )
        }

        for key, factory in model_factories.items():
            if key in self.model_name.lower():
                return factory()
        raise TypeError(f"unsupported model: {self.model_name}")


    # ========================= REACT AGRNT ========================= #
    def get_react_executor(self, prompt_type:str):
        """
        get react executor
        """
        new_llm = self.get_model()
        # react_prompt_template = hub.pull("hwchase17/react")
        raw_prompt_template = self.load_prompt(prompt_type, True) # use our own prompt
        react_prompt_template = PromptTemplate.from_template(raw_prompt_template)

        new_agent = create_react_agent(
            llm=new_llm, 
            tools=self.tools, 
            prompt=react_prompt_template,
            ) 
        executor = AgentExecutor(
            agent=new_agent, 
            tools=self.tools, 
            verbose=True,
            output_parser=NoOpOutputParser(),
            handle_parsing_errors=True,
            )
        return executor

    def invoke_react_agent(self, prompt_type:str, input:Dict[str,str], config:Dict[str,str]) -> dict:
        """
        invoke a react agent
        args:
            prompt_type: One of ["evaluate", "generate", "regenerate"]
            input: dictonary to fill all the placeholders in prompt
            config: configs of agent for example: {"configurable": {"thread_id": "2"}}
        """
        raw_prompt_template = self.load_prompt(prompt_type, True) # use our own prompt
        react_prompt_template = _replace_placeholder(raw_prompt_template, input["input"],placeholder="{input}")

        agent_executor = self.get_react_executor(prompt_type)
        result = agent_executor.invoke(
            input=input, 
            config=config, 
            handle_parsing_errors=True,
            )

        return result.get("output"), react_prompt_template


    # ========================= SIMPLE AGRNT ========================= #
    def invoke_simple_agent(self, prompt_type:str, input:Dict[str,str], config:Dict[str,str], ext_prompt=False) -> str:
        """
        invoke a regular agent
        args:
            prompt_type: One of ["evaluate", "generate", "regenerate","final_test"], if ext_prompt = True, you should fill your own prompt here
            input: dictonary to fill all the placeholders in prompt
            config: configs of agent for example: {"configurable": {"thread_id": "2"}}
            ext_prompt: when using other prompt --> True, in this case, prompt_type = prompt_string
        """
        if not ext_prompt:
            raw_prompt_template = self.load_prompt(prompt_type, False)
        else:
            raw_prompt_template = prompt_type
        chatprompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
            ("human", raw_prompt_template)
        ])
        formatted_prompt = chatprompt_template.format(**input)

        new_llm = self.get_model()        
        chain:Runnable = chatprompt_template | new_llm | StrOutputParser()
        result = chain.invoke(input=input, config=config)
        return result, formatted_prompt
    

    # ========================= DOUBLECHAIN AGRNT ========================= #
    def invoke_doublechain_agent(self, prompt_type: str, input: Dict[str, str], config: Dict[str, str], ext_prompt=False) -> Tuple[str, str]:
        """
        Invoke a double-chain agent that separates code generation and formatting
        
        args:
            prompt_type: One of ["evaluate", "generate", "regenerate", "final_test"], if ext_prompt = True, you should fill your own prompt here
            input: dictionary to fill all the placeholders in prompt
            config: configs of agent for example: {"configurable": {"thread_id": "2"}}
            ext_prompt: when using other prompt --> True, in this case, prompt_type = prompt_string
        
        returns:
            Tuple of (resulting output, formatted prompt)
        """
        # Get the appropriate prompt template
        # if not ext_prompt:
        #     raw_prompt_template = self.load_prompt(prompt_type, False)
        # else:
        #     raw_prompt_template = prompt_type
        
        # First chain: Generate the Problog code with tools
        first_input = {
            "template_code": input["input"],
            "agent_scratchpad": ""
        }
        prompt_msgs = [
            ("system", "You are a coding assistant. Use the tools as needed to complete the ProbLog code."),
            ("human", """You are an expert programmer proficient in Problog and DeepProbLog. Your task is to generate the complete code based on the user's requirements in each <langda> block.
<Code>
{template_code}
</Code>
<Final_Answer> The generated completed code should be formatted as follows:
// other contents
```problog
//the completed original code here
```
</Final_Answer>"""),
            ("assistant", "{agent_scratchpad}")  # where tool outputs and thoughts will appear
        ]
        first_chain_prompt = ChatPromptTemplate.from_messages(prompt_msgs)
        first_formatted_prompt = first_chain_prompt.format_prompt(**first_input).to_string()
        # Create the model for generation
        new_llm = self.get_model()
        agent = create_tool_calling_agent(new_llm, self.tools, first_chain_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        # Execute the first chain
        print("Executing first chain: Code generation with tools...")
        first_result = agent_executor.invoke(input=first_input, config=config)
        generated_result = first_result.get("output", "")

        # Second chain: Format the code output correctly
        generated_code = ""
        pattern = r"```(?:problog|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, generated_result, re.DOTALL)
        for match in matches:
            generated_code += match
            generated_code += "\n\n"
        second_input = {
            "origin_code": input["input"],
            "generated_code": generated_code.strip()
        }
        second_chain_prompt = PromptTemplate.from_template("""
In section <origin_code> and <generated_code> you will be give two codes,
- in <origin_code> there's incomplete code with <langda> blocks.
- in <generated_code> there's completed code of <origin_code>.
your task is to extract and format each code block in <generated_code> that corresponds to the <langda> blocks in <origin_code>
<origin_code>
{origin_code}
</origin_code>
<generated_code>
{generated_code}
<generated_code>
<Final_Answer> Each code block SHOULD ONLY CONTAINS THE EXACT CONTENT of <langda> blocks, for example:
for the following original code:
<Code>
head(X) :-
<Langda> Information of 1st Placeholder:
<HASH> Hash tag of code: XXXXABCD </HASH>
<LLM> Requirements of Rules:...  </LLM></Langda>
//other contents...
</Code>
if you extracted code contains "head(X) :-", it's wrong, because it's OUTSIDE the <langda> block

For each code block , extract it and format it as follows:
```problog
{{"HASH": "XXXX1234","Code": "Completed code snippet 1"}}
```
```problog
{{"HASH": "XXXX3456","Code": "Completed code snippet 2"}}
```
</Final_Answer>""")
        second_formatted_prompt = second_chain_prompt.format_prompt(**second_input).to_string()
        # Execute the second chain
        print("Executing second chain: Code formatting...")
        format_chain = second_chain_prompt | new_llm | StrOutputParser()
        formatted_result = format_chain.invoke(input=second_input, config=config)

        return formatted_result, first_formatted_prompt + "\n\n" + second_formatted_prompt