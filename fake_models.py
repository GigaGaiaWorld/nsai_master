from typing import Literal, Dict, List, Tuple
from pydantic import BaseModel, Field

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import time
import re

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

from dotenv import find_dotenv

def retry_agent(max_attempts):
    # Allow the agent retry 2 times
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts:
                        time.sleep(1)
                    else:
                        raise e
        return wrapper
    return decorator

class NoOpOutputParser(BaseOutputParser[str]):
    def parse(self, text: str) -> str:
        return text

    def get_format_instructions(self) -> str:
        return ""

class LLMConfig(BaseModel):
    model: str
    api_key: str
    api_typ: str = "Bearer"
    api_ver: str = "2024-01-01"
    temperature: float = 0.2

class AgentSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
        # env_prefix="gnrt_",
        env_nested_delimiter="_",
        env_nested_max_split = 1,
        extra="ignore"
    )
    deepseek: LLMConfig # 1. subconfig：DeepSeek
    openai: LLMConfig   # 2. subconfig：OpenAI
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
    prompt_format: Dict[str, str] = Field(default={
        "generate": "generate_prompt_{}.txt",
        "evaluate": "evaluate_prompt_{}.txt",
        "regenerate": "regenerate_prompt_{}.txt",
        "final_test": "zfinaltest_prompt_simple.txt",
    })

    def get_prompt_path(self, prompt_type: str, agent_type:str) -> Path:
        """
        Get path for prompt files.
        Args:
            prompt_type: One of ["evaluate", "generate", "regenerate"]
        """
        if prompt_type not in self.prompt_format:
            raise FileExistsError(f"Unknown prompt: {prompt_type}.")
        return Path(__file__).parent.parent / "prompts" / self.prompt_format[prompt_type].format(agent_type)

    def load_prompt(self, prompt: Literal["evaluate", "generate", "regenerate", "final_test"], agent_type:str) -> str:
        """
        Load prompt content from file.
        Args:
            prompt: One of ["evaluate", "generate", "regenerate", "final_test"]
            usereact: use react prompt or not
        """
        path = self.get_prompt_path(prompt, agent_type)
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


    # ========================= SIMPLE AGRNT ========================= #
    @retry_agent(max_attempts=3)
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
            raw_prompt_template = self.load_prompt(prompt_type, "simple")
        else:
            raw_prompt_template = prompt_type
        chatprompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a coding assistant. You could complete the task with your knowledge."),
            ("human", raw_prompt_template)
        ])
        if not(prompt_type == "final_test"):
            simple_input = {"input":input["prompt_template"]}
        else:
            simple_input = input

        formatted_prompt = chatprompt_template.format_prompt(**simple_input).to_string()

        new_llm = self.get_model()
        chain:Runnable = chatprompt_template | new_llm | StrOutputParser()
        result = chain.invoke(input=simple_input, config=config)
        return result, formatted_prompt, ""
    

    # ========================= REACT AGRNT ========================= #
    def get_react_executor(self, prompt_type:str):
        """
        get react executor
        """
        new_llm = self.get_model()
        # react_prompt_template = hub.pull("hwchase17/react")
        raw_prompt_template = self.load_prompt(prompt_type, "react") # use our own prompt
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
            max_iterations = 5
            )
        return executor

    @retry_agent(max_attempts=3)
    def invoke_react_agent(self, prompt_type:str, input:Dict[str,str], config:Dict[str,str]) -> dict:
        """
        invoke a react agent
        args:
            prompt_type: One of ["evaluate", "generate", "regenerate"]
            input: dictonary to fill all the placeholders in prompt
            config: configs of agent for example: {"configurable": {"thread_id": "2"}}
        """
        react_input = {
            "input": input["prompt_template"],
            "agent_scratchpad": ""
        }

        agent_executor = self.get_react_executor(prompt_type)
        result = agent_executor.invoke(
            input=react_input, 
            config=config, 
            handle_parsing_errors=True,
            )

        return result.get("output"), "", ""



    def extracted_first_result(self, input):
        return input

    def split_doublechain_prompt(self,prompt_template:str):
        lines = prompt_template.split("*** split ***")
        return lines[0], lines[1]

    @retry_agent(max_attempts=3)
    def invoke_doublechain_agent(self, prompt_type: str, input: Dict[str, str], config: Dict[str, str]) -> str:
        raw_prompt_template = prompt_type
        new_llm = self.get_model()
        # *** First chain: Generate the Problog code with tools *** 
        first_chain_prompt_template, second_chain_prompt_template = self.split_doublechain_prompt(raw_prompt_template)
        if prompt_type == "regenerate":
            system_prompt = ("system", """You are a coding assistant. You could use the available tools to complete the task,
                            you should always use 'get_report_tool' first to gain more information.""")
        elif prompt_type == "generate" or prompt_type == "evaluate":
            system_prompt = ("system", "You are a coding assistant. You should use the available tools to complete the task.")
        first_input = {
            "input": input["prompt_template"],
            "agent_scratchpad": ""
        }
        prompt_msgs = [
            system_prompt,
            ("human", first_chain_prompt_template),
            ("assistant", "{agent_scratchpad}")  # where tool outputs and thoughts will appear
        ]
        first_chain_prompt = ChatPromptTemplate.from_messages(prompt_msgs)
        # Execute the first chain
        agent = create_tool_calling_agent(new_llm, self.tools, first_chain_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        first_result_raw = agent_executor.invoke(input=first_input, config=config)
        first_result = first_result_raw.get("output", "")

        # *** Second chain: Format the code output correctly ***
        extracted_result = self.extracted_first_result(first_result)
        second_input = {
            "template_code": input["prompt_template"],
            "first_chain_output": extracted_result.strip()
        }
        second_chain_prompt = PromptTemplate.from_template(second_chain_prompt_template)
        # Execute the second chain
        format_chain = second_chain_prompt | new_llm | StrOutputParser()
        second_result = format_chain.invoke(input=second_input, config=config)
        
        return second_result






    @retry_agent(max_attempts=3)
    def invoke_react_agent(self, prompt_type:str, input:Dict[str,str], config:Dict[str,str]) -> str:
        react_input = {
            "input": input["prompt_template"],
            "agent_scratchpad": ""
        }
        new_llm = self.get_model()
        raw_prompt_template = self.load_prompt(prompt_type, "react")
        react_prompt_template = PromptTemplate.from_template(raw_prompt_template)
        # Execute Agent: 
        new_agent = create_react_agent(llm=new_llm, tools=self.tools, prompt=react_prompt_template) 
        agent_executor = AgentExecutor(
            agent=new_agent, 
            tools=self.tools, 
            verbose=True,
            output_parser=NoOpOutputParser(), 
            max_iterations=5)
        result = agent_executor.invoke(input=react_input, config=config, handle_parsing_errors=True)
        return result.get("output")
    
state = []
tools = []
prompt_type = 
def invoke_agent(...):
    return

generated_result, formatted_prompt, _ = invoke_agent(
    agent_type=state["agent_type"]["generate"], 
    model_name=state["model_name"], 
    tools=state["tools"], 
    prompt_type=prompt_type, 
    input=input, 
    config=state["config"])