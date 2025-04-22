#! /usr/bin/env python3
from cabinet import Cabinet
from openai import OpenAI

cabinet = Cabinet()

class ChatGPT:
    def __init__(self):
        self.client = OpenAI(api_key=cabinet.get("keys", "openai"))

    def query(self, prompt: str) -> str:
        """Query ChatGPT with a given prompt."""
        response = self.client.responses.create(
            model="gpt-4o",
            input=[
                {
            "role": "system",
            "content": [
                {
                "type": "input_text",
                "text": prompt
                }
            ]
            }
        ],
        text={
            "format": {
            "type": "text"
            }
        },
        reasoning={},
        tools=[],
            temperature=1,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )

        return response.output_text.strip() if response.output_text else "0"