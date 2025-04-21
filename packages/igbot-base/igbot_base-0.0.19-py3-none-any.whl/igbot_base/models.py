from enum import Enum
from openai import OpenAI


class ModelInfo:

    def __init__(self, name, client):
        self.__name = name
        self.__client = client

    def get_name(self):
        return self.__name

    def get_client(self):
        return self.__client()


class Model(Enum):
    OLLAMA_3_2_LOCAL = ModelInfo("llama3.2", lambda: OpenAI(base_url="http://localhost:11434/v1", api_key='ollama'))
    OPENAI_GPT_4o_MINI = ModelInfo("gpt-4o-mini", lambda: OpenAI())
    OPENAI_GPT_4o = ModelInfo("gpt-4o", lambda: OpenAI())
    OPENAI_GPT_4o_MINI_JSON = ModelInfo("gpt-4o-mini-2024-07-18", lambda: OpenAI())
