# By default, the environment variable name is the same as the field name.
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel
from typing import ClassVar
# src/config/settings.py
from pydantic import Field, HttpUrl
from pathlib import Path


class LLMConfig(BaseModel):
    # provider: str
    api_key: str = "ask"
    # api_type: str
    # api_version: str

class DeepSeekGeneratorModel(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        env_prefix="gnrt_deepseek",
        env_nested_max_split=1
    )
    llm:LLMConfig


print(DeepSeekGeneratorModel().model_dump())
