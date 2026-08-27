# Please install OpenAI SDK first: `pip3 install openai python-dotenv`
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=os.environ.get('DEEPSEEK_BASE_URL', "https://api.deepseek.com")
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "你是一个翻译助手，帮我将用户给出的英文翻译为中文"},
        {"role": "user", "content": "Ethereum is a decentralized network"},
    ],
    stream=False
)

print(response.choices[0].message.content)