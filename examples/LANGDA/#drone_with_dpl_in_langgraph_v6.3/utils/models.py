from typing import Literal, Dict, List
from pydantic import BaseModel, Field

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from langchain import hub
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

    def react_prompt_input(self, type:str) -> str:
        if type == "evaluate":
            return """First, the complete code is given below:

{output}

Next, here are the generated code segments:

{code_list}"""
        elif type == "evaluate_with_test_result":
            return """<question>You are an expert reviewer proficient in Problog and neuro-symbolic systems. Your task is to analyze each completed Prolog code block below and determine whether it satisfies the user's original design intentions for Langda.
<rule_set>
            First, the complete code is given below:

{output}
</rule_set>
<code_list>
Next, here are the generated code segments:

{code_list}
</code_list>
<test_result>
Next, here are the test result of the code:

{test_result}
</test_result>
</question>"""
        elif type == "generate":
            return """<question>You are an expert programmer proficient in Problog and DeepProbLog. Your task is to generate code to complete the placeholders marked as {{LANGDA}} based on the user's requirements.
<rule_set>
Below is the DeepProbLog code, with some parts represented by the placeholder {{LANGDA}}:

{rule_set}
</rule_set>
<requirements>
Below are the user's natural language description and rule explanation:

{requirements}
</requirements>
</question>"""
        elif type == "regenerate":
            return """<question>You are an expert programmer proficient in Problog and DeepProbLog. Your task is to regenerate the code to fill in the {{LANGDA}} placeholders, based on the information of current used code segments.
<rule_set>
Below is the DeepProbLog code with some parts represented by the placeholder {{LANGDA}}:

{rule_set}
</rule_set>
<requirements>
Below are the currently used code segments for each placeholder {{LANGDA}} and their analysis results:

{requirements}
</requirements>
</question>"""

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
        react_prompt_type = prompt_type
        if "test_result" in input and prompt_type == "evaluate":
            react_prompt_type = "evaluate_with_test_result"
        
        prompt_template = PromptTemplate.from_template(self.react_prompt_input(react_prompt_type))
        formatted_prompt = prompt_template.format_prompt(**input).to_string()

        invoke_params = {"input": formatted_prompt}

        agent_executor = self.get_react_executor(prompt_type)
        result = agent_executor.invoke(
            input=invoke_params, 
            config=config, 
            handle_parsing_errors=True,
            )

        return result.get("output"), invoke_params

    def invoke_agent(self, prompt_type:str, input:Dict[str,str], config:Dict[str,str], ext_prompt=False) -> str:
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