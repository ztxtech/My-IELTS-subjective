import os

from colorama import init, Fore
from openai import OpenAI

# 初始化colorama
init(autoreset=True)

class OpenAIBase:
    # 定义类变量作为默认值
    name = 'name'
    base_url = 'base_url'
    api_env = "ENV_API_KEY"

    def __init__(self, model='model', api_key=None, system_prompts=None, silent=True):
        # 使用类变量作为默认值
        self.name = self.__class__.name
        self.base_url = self.__class__.base_url
        self.api_env = self.__class__.api_env

        if not api_key:
            self.api_key = os.environ.get(self.api_env)
        else:
            self.api_key = api_key

        self.model = model
        self.system_prompts = system_prompts
        self.silent = silent

        self.client = None

    def init_cilent(self):
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

        print("\n" * 2)
        print(Fore.GREEN + f'{self.name} initialized with model: {self.model}')
        print(Fore.YELLOW + "-" * 20)
        self.history = []
        if self.system_prompts:
            for prompt in self.system_prompts:
                self.history.append({"role": "system", "content": prompt})
            if not self.silent:
                print(Fore.CYAN + f'System: {"\n".join(self.system_prompts)}')

    def wait(self):
        pass

    def generate_content(self, parts):
        if not self.client:
            self.init_cilent()
            
        user_message = {"role": "user", "content": "\n".join(parts)}
        self.history.append(user_message)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history
        )

        assistant_message = response.choices[0].message
        self.history.append({"role": "assistant", "content": assistant_message.content})

        print(Fore.BLUE + f'User: {"\n".join(parts)}')
        print(Fore.MAGENTA + f'{self.name}: {assistant_message.content}')
        print(Fore.RED + f'TOKEN CONSUME: {response.usage.total_tokens}')
        print(Fore.YELLOW + '-' * 20)
        return assistant_message.content

    def fail(self):
        self.history.pop()

    def clear_client(self):
        self.client = None