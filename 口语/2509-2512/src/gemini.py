import math
import os
import time

from google import genai
from google.genai.types import Part


class Gemini:
    def __init__(self, model='gemini-2.5-flash', api_key=None, system_prompts=None):

        if not api_key:
            self.api_key = os.environ.get('GEMINI_API_KEY')
        else:
            self.api_key = api_key

        self.model = model
        self.client = genai.Client(api_key=self.api_key)
        print("\n" * 2)
        print('Gemini initialized with model: {}'.format(self.model))
        print("-" * 20)
        self.history = []
        if system_prompts:
            temp = {'role': 'user', 'parts': []}
            for prompt in system_prompts:
                temp['parts'].append(Part.from_text(text=prompt))
            self.history.append(temp)
            print(f'System: {'\n'.join(system_prompts)}')

    def wait(self):
        rpm_dict = {
            "gemini-2.5-pro": 5,
            "gemini-2.5-flash": 10,
            "gemini-2.5-flash-lite": 15,
            "gemini-2.0-flash": 15,
            "gemini-2.0-flash-lite": 30
        }
        time.sleep(math.ceil(60.0 / rpm_dict[self.model]) + 5)

    def generate_content(self, parts):
        user_parts = {'role': 'user', 'parts': []}
        for prompt in parts:
            user_parts['parts'].append(Part.from_text(text=prompt))
        self.history.append(user_parts)

        response = self.client.models.generate_content(
            model=self.model, contents=self.history
        )
        self.history.append({'role': 'model', 'parts': [Part.from_text(text=response.text)]})

        print(f'User: {'\n'.join(parts)}')
        print(f'Gemini: {response.text}')
        print(f'TOKEN CONSUME: {response.usage_metadata.total_token_count}')
        print('-' * 20)
        return response.text

    def fail(self):
        self.history.pop()
