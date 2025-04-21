# ShangshanAI SDK

一个用于下载和处理数据的Python SDK。

## 安装

```bash
pip install shangshanAI
```

## 下载模型

```python
from shangshanAI import snapshot_download
model_dir = snapshot_download('testuser/model_llm')
print(model_dir)
```

## 功能特性

- 支持文件下载
- 自动重试机制
- 进度显示

## 调用大模型

```python
from shangshanAI import ShangshanAI

client = ShangshanAI(api_key="BkdNcaHp6YUxvYsp6PpzMq", path="/v1/chat/completions")  # 请填写您自己的API Key
response = client.chat.completions.create(
    model="shangshan-chat-beta",  # 填写需要调用的模型编码
    messages=[
        {"role": "user", "content": "你好！你叫什么名字"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
```

## 许可证

MIT License