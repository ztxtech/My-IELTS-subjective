import time

from src.llm.base.openai import OpenAIBase


class ModelScope(OpenAIBase):
    name = 'ModelScope'
    base_url = 'https://api-inference.modelscope.cn/v1/'
    api_env = 'MODELSCOPE_API_KEY'
    # default_model = 'moonshotai/Kimi-K2-Instruct'
    default_model = 'deepseek-ai/DeepSeek-V3.1'
    # default_model = 'Qwen/Qwen3-235B-A22B-Instruct-2507'
    # default_model = 'ZhipuAI/GLM-4.5'

    temperature = 0.7
    top_p = 0.9

    def __init__(self, model=default_model, api_key=None, system_prompts=None, silent=True):
        super().__init__(model, api_key, system_prompts, silent)

    def wait(self):
        time.sleep(2)
