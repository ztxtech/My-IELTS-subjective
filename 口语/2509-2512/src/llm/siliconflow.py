import time

from src.llm.base.openai import OpenAIBase


class SiliconFlow(OpenAIBase):
    name = 'SiliconFlow'
    base_url = 'https://api.siliconflow.cn/v1'
    api_env = "SILICONFLOW_API_KEY"
    default_model = 'Qwen/Qwen3-8B'

    def __init__(self, model=default_model, api_key=None, system_prompts=None, silent=True):
        super().__init__(model, api_key, system_prompts, silent)

    def wait(self):
        time.sleep(10)
