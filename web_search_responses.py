import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=os.environ.get('DEEPSEEK_BASE_URL', "https://api.deepseek.com")
)

# 提示词：要求大模型利用 web_search 联网检索能力
prompt = "请帮看看 https://news.ycombinator.com/ 最新的一条新闻是什么？"

print(f"User>\t {prompt}\n")
print("Model (Streaming)> \n")

# 使用 OpenAI Responses API 发起流式请求 (stream=True)，开启服务端的 web search 检索能力
response_stream = client.responses.create(
    model="deepseek-v4-flash",
    tools=[{"type": "web_search"}],
    input=prompt,
    stream=True
)

# 实时处理流式事件增量输出
for event in response_stream:
    if event.type == "response.output_text.delta":
        # 实时输出回答文本
        print(event.delta, end="", flush=True)

print("\n")
