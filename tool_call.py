import os
import json
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=os.environ.get('DEEPSEEK_BASE_URL', "https://api.deepseek.com")
)

def print_separator(title=""):
    print("\n " + title  )

def print_message_detail(role: str, content: str = None, extra: dict = None):
    """格式化打印单条角色的详细日志"""
    print(f"\n👉 [{role.upper()}]")
    if content:
        print(f"Content:\n{content}")
    if extra:
        for k, v in extra.items():
            print(f"{k}:\n{v}")

def log_conversation_context(messages, step_name=""):
    """打印当前上下文中所有消息的快照"""
    print_separator(f"{step_name}")
    for idx, msg in enumerate(messages, 1):
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content")
            extra = {}
            if "tool_call_id" in msg:
                extra["tool_call_id"] = msg["tool_call_id"]
        else:
            # ChatCompletionMessage 对象
            role = msg.role
            content = msg.content
            extra = {}
            if msg.tool_calls:
                extra["tool_calls"] = [
                    {
                        "id": tc.id,
                        "function": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                    for tc in msg.tool_calls
                ]
        print(f"[{idx}] Role: {role.upper()}")
        if content:
            print(f"    Content: {content}")
        if extra:
            for k, v in extra.items():
                print(f"    {k}: {v}")
    print("=" * 70 + "\n")

# 1. 本地可执行的真实函数：执行 Shell 命令
def run_command(command: str) -> str:
    """执行本地命令行指令并返回输出结果"""
    print(f"\n⚙️ [Tool Local Execution] 正在执行本地命令: `{command}`")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout if result.returncode == 0 else result.stderr
        return output.strip()
    except Exception as e:
        return f"Error executing command: {e}"

# 2. 定义 Tool (Function Calling) 的元数据声明
tools = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "执行本地 Shell 命令（如 ls、cat 等）并获取控制台输出",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "需要执行的命令行指令，例如 'ls'",
                    }
                },
                "required": ["command"]
            },
        }
    },
]

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

# 3. 发起用户提问 (Round 1)
user_prompt = "请帮我查看当前目录下是否包含 Readme 相关文件？"
messages = [{"role": "user", "content": user_prompt}]

log_conversation_context(messages, "Round 1: 用户发起提问")
message = send_messages(messages)

# 4. 判断模型返回内容：是直接回答还是请求工具调用
if message.tool_calls:
    tool_call = message.tool_calls[0]
    print_message_detail(
        role="assistant (tool_call_request)",
        content=message.content,
        extra={
            "tool_call_id": tool_call.id,
            "function_name": tool_call.function.name,
            "arguments": tool_call.function.arguments
        }
    )
    
    # 本地执行工具
    arguments = json.loads(tool_call.function.arguments)
    command = arguments.get("command", "ls")
    tool_result = run_command(command)
    
    # 打印工具执行结果
    print_message_detail(
        role="tool (execution_result)",
        content=tool_result,
        extra={"tool_call_id": tool_call.id}
    )
    
    # 将模型消息与工具执行结果压入上下文列表
    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": tool_result
    })
    
    # 5. 第二次请求：将包含工具结果的完整上下文发送给模型 (Round 2)
    log_conversation_context(messages, "发送 Round 2 (包含工具结果) ")
    print_separator("Round 2: 回传工具结果，获取最终回答")
    
    final_message = send_messages(messages)
    messages.append(final_message)
    
    print_message_detail(role="assistant (final_answer)", content=final_message.content)
