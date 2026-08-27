# AI Demo

## 环境安装

```bash

# 默认使用 ARM64 原生 Python 3.12 创建虚拟环境
python -m venv myenv 或 uv venv myenv --python 3.12

# 激活虚拟环境
source myenv/bin/activate

pip install openai python-dotenv 或 uv pip install openai python-dotenv --python myenv
```


## 环境配置
 
```bash
cp env_sample .env
```

修改 `DEEPSEEK_API_KEY`

## 运行示例

```bash
# 单轮对话 Demo
python simple_chat.py

# 多轮对话 Demo
python multi_chat.py

# 工具调用 (Tool Calls / Function Calling) Demo
python tool_call.py

# Responses API + Web Search 服务端联网搜索 Demo
python web_search_responses.py
```