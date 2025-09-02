import time

from src.llm.base.openai import OpenAIBase


class Openrouter(OpenAIBase):
    name = 'Openrouter'
    base_url = 'https://openrouter.ai/api/v1'
    api_env = 'OPENROUTER_API_KEY'
    default_model = 'qwen/qwen3-235b-a22b:free'

    def __init__(self, model=default_model, api_key=None, system_prompts=None, silent=True):
        super().__init__(model, api_key, system_prompts, silent)

    def wait(self):
        time.sleep(30)
