import time

from src.llm.base.openai import OpenAIBase


class ModelScope(OpenAIBase):
    name = 'ModelScope'
    base_url = 'https://api-inference.modelscope.cn/v1/'
    api_env = 'MODELSCOPE_API_KEY'
    default_model = 'moonshotai/Kimi-K2-Instruct'

    def __init__(self, model=default_model, api_key=None, system_prompts=None, silent=True):
        super().__init__(model, api_key, system_prompts, silent)

    def wait(self):
        time.sleep(10)
