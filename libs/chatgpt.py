import os

import openai


class Gpt:
    engine = "gpt-3.5-turbo"

    def __init__(self):
        openai.api_key = os.getenv("GPT_TOKEN")

    def check_gpt(self, message: str):

        completion = openai.ChatCompletion.create(
            model=self.engine, messages=[{"role": "user", "content": message}]
        )

        return completion.choices[0].message.content
