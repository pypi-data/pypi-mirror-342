# metaso-sdk

[![ci](https://github.com/meta-sota/metaso-sdk/workflows/ci/badge.svg)](https://github.com/meta-sota/metaso-sdk/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://meta-sota.github.io/metaso-sdk/)
[![pypi version](https://img.shields.io/pypi/v/metaso-sdk.svg)](https://pypi.org/project/metaso-sdk/)

[秘塔AI搜索](https://metaso.cn) Python SDK。在使用这个 SDK 之前，请先通过[API文档专题](https://metaso.cn/s/hXHmJkx)了解 HTTP 接口的更多细节。

## 安装

```bash
pip install metaso-sdk
```

## 配置 METASO_API_KEY

metaso-sdk 从环境变量 `METASO_API_KEY` 读取用于认证的 API 密钥，可以在 shell 里进行设置：

```bash
export METASO_API_KEY="mk-EE2..."
```

或者在 Python 代码里进行设置：

```python
import os
os.environ["METASO_API_KEY"] = "mk-EE2..."
```

## 搜索

### 搜索问题
```python
from metaso_sdk import search, Query
search(Query(question="abc"))
```

### 追问

```python
search(Query(question="广播公司", sessionId="8550018047390023680"))
```

### 流式返回

```python
for chunk in search(Query(question="abc"), stream=True):
    print(chunk)

...
{'type': 'heartbeat'}
{'text': '因此，“abc”可以指代字母表的前三个字母、美籍华裔、美国广播公司、一种音乐记谱法以及一种编程语言。具体含义需要根据上下文来确定。', 'type': 'append-text'}
```

## 专题

### 递归上传文件夹

```
from metaso_sdk import create_topic, upload_directory, Topic

topic = create_topic(Topic(name="functional programing"))
files = upload_directory(topic, "dir")
```

### 搜索特定专题

```python
from metaso_sdk import search, Query

query = Query(question="functional")
search(query, topic=topic)
```
