import os

import openai
from g4f.client import Client

class Gpt:
    engine = "gpt-3.5-turbo"

    def __init__(self):
        #openai.api_key = os.getenv("GPT_TOKEN")
        self.client = Client()

    def check_gpt(self, message: str):

        completion = self.client.chat.completions.create(
            model=self.engine, messages=[{"role": "user", "content": message + ". Напиши по русски."}]
        )

        return completion.choices[0].message.content
