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
            ("system", "You are an expert programmer proficient in Problog and DeepProbLog. You could complete the task with your knowledge."),
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


    # ========================= DOUBLECHAIN AGRNT ========================= #
    def split_doublechain_prompt(self,prompt_template:str):
        lines = prompt_template.split("*** split ***")
        return lines[0], lines[1]
    
    @retry_agent(max_attempts=3)
    def invoke_doublechain_agent(self, prompt_type: str, input: Dict[str, str], config: Dict[str, str], ext_prompt=False) -> Tuple[str, str]:
        """
        Invoke a double-chain agent that separates code generation and formatting
        
        args:
            prompt_type: One of ["evaluate", "generate", "regenerate"], if ext_prompt = True, you should fill your own prompt here
            input: dictionary to fill all the placeholders in prompt
            config: configs of agent for example: {"configurable": {"thread_id": "2"}}
            ext_prompt: when using other prompt --> True, in this case, prompt_type = prompt_string

        returns:
            Tuple of (resulting output, formatted prompt, result from first chain)
        """
        # Get the appropriate prompt template
        if not ext_prompt:
            raw_prompt_template = self.load_prompt(prompt_type, "doublechain")
        else:
            raw_prompt_template = prompt_type

        new_llm = self.get_model()


        # *** First chain: Generate the Problog code with tools *** 

        # TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK
        first_chain_prompt_template, second_chain_prompt_template = self.split_doublechain_prompt(raw_prompt_template)
        if prompt_type == "generate":
            system_prompt = ("system", "You are an expert programmer proficient in Problog and DeepProbLog. You could use the available tools to complete the task.")
        elif prompt_type == "evaluate":
            system_prompt = ("system", "You are an expert code evaluator specialized in ProbLog and DeepProbLog. You could use the available tools to complete the task.")
        elif prompt_type == "regenerate":
            system_prompt = ("system", "You are an expert programmer proficient in Problog and DeepProbLog. You could use the available tools to complete the task. You should always use 'get_report_tool' first to gain more information.")

        # *** Test double chain without tools: *** #
        # first_chain_prompt_template, second_chain_prompt_template = self.split_doublechain_prompt(raw_prompt_template)
        # if prompt_type == "generate":
        #     system_prompt = ("system", "You are an expert programmer proficient in Problog and DeepProbLog. You should complete the task.")
        # elif prompt_type == "evaluate":
        #     system_prompt = ("system", "You are an expert code evaluator specialized in ProbLog and DeepProbLog. You should complete the task.")
        # elif prompt_type == "regenerate":
        #     system_prompt = ("system", "You are an expert programmer proficient in Problog and DeepProbLog. You should always use 'get_report_tool' first to gain more information.")

        # TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK

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
        first_formatted_prompt = first_chain_prompt.format_prompt(**first_input).to_string()
        # Create the model for generation

        # TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK
        # *** CASE1: Test double chain without tools: *** # 
        print("Executing first chain: Code generation with tools...")
        if prompt_type == "evaluate":
            format_chain_first = first_chain_prompt | new_llm | StrOutputParser()
            first_result = format_chain_first.invoke(input=first_input, config=config)
        elif prompt_type == "generate" or prompt_type == "regenerate":
            agent = create_tool_calling_agent(new_llm, self.tools, first_chain_prompt)
            agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
            # Execute the first chain
            first_result_raw = agent_executor.invoke(input=first_input, config=config)
            first_result = first_result_raw.get("output", "")
        # *** CASE2: Test double chain with tools: *** #
        # agent = create_tool_calling_agent(new_llm, self.tools, first_chain_prompt)
        # agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        # TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK ====== TEST BLOCK

        # *** Second chain: Format the code output correctly ***
        extracted_result = ""
        if prompt_type == "evaluate":
            extracted_result = first_result
        elif prompt_type == "generate" or prompt_type == "regenerate":
            pattern = r"```(?:problog|[a-z]*)?\n(.*?)```"
            matches = re.findall(pattern, first_result, re.DOTALL)
            extracted_result = matches[-1]
            print("*** Generated New Code ***\n",extracted_result)
        second_input = {
            "template_code": input["prompt_template"],
            "first_chain_output": extracted_result.strip()
        }
        second_chain_prompt = PromptTemplate.from_template(second_chain_prompt_template)
        second_formatted_prompt = second_chain_prompt.format_prompt(**second_input).to_string()
        # Execute the second chain
        print("Executing second chain: Code formatting...")
        format_chain = second_chain_prompt | new_llm | StrOutputParser()
        second_result = format_chain.invoke(input=second_input, config=config)

        return second_result, first_formatted_prompt + "\n\n**split**\n\n" + second_formatted_prompt, extracted_result


