from typing import Literal, Dict
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from langchain import hub
from langchain.schema.runnable import Runnable
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

class LangdaAgentExecutor:
    """
    when creating, you should give the model_name and tools
    invoke_react_agent: reactive agent
    invoke_agent:       regular agent
    """
    def __init__(self, model_name:str, tools:list):
        self.cfgs = AgentSettings()
        self.tools = tools
        self.model_name = model_name

    def get_model(self):

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
        raise ValueError(f"unsupported model: {self.model_name}")

    def get_react_executor(self):
        """
        """
        new_llm = self.get_model()
        react_prompt = hub.pull("hwchase17/react")
        new_agent = create_react_agent(llm=new_llm, tools=self.tools, prompt=react_prompt)
        executor = AgentExecutor(agent=new_agent, tools=self.tools, verbose=True)
        return executor


    def invoke_react_agent(self, prompt_type:str, input:Dict[str,str], config:Dict[str,str]) -> dict:
        """
        invoke a react agent
        Args:
            prompt_type: One of ["evaluate", "generate", "regenerate"]
            input: dictonary to fill all the placeholders in prompt
            config: configs of agent for example: {"configurable": {"thread_id": "2"}}
        """
        agent_executor = self.get_react_executor()
        raw_prompt_template = paths.load_prompt(prompt_type)

        
        prompt_template = PromptTemplate.from_template(raw_prompt_template)
        formatted_prompt = prompt_template.format_prompt(**input)

        result = agent_executor.invoke(input={"input":formatted_prompt}, config=config, handle_parsing_errors=True)
        return result


    def invoke_agent(self, prompt_type:str, input:Dict[str,str], config:Dict[str,str], ext_prompt=False) -> str:
        """
        invoke a regular agent
        Args:
            prompt_type: One of ["evaluate", "generate", "regenerate","final_test"], if ext_prompt = True, you should fill your own prompt here
            input: dictonary to fill all the placeholders in prompt
            config: configs of agent for example: {"configurable": {"thread_id": "2"}}
            ext_prompt: when using other prompt --> True, in this case, prompt_type = prompt_string
        """
        if not ext_prompt:
            raw_prompt_template = paths.load_prompt(prompt_type)
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