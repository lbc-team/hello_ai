# AI Demo

## 环境安装

```bash

# 默认使用 ARM64 原生 Python 3.11 创建虚拟环境
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