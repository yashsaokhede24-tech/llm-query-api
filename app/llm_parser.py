import openai
import os

class LLMParser:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def parse(self, question: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal/compliance/insurance document expert. Parse the question and return a clear, structured query."},
                {"role": "user", "content": question}
            ],
            max_tokens=100,
            temperature=0.2
        )
        return response["choices"][0]["message"]["content"].strip()