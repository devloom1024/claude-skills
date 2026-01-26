# Firecrawl SDK 参考

## 安装

```bash
pip install firecrawl-py python-dotenv
```

## API Key 配置

```python
from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件
api_key = os.environ.get("FIRECRAWL_API_KEY")
```

或直接传递：

```python
from firecrawl import Firecrawl
firecrawl = Firecrawl(api_key="fc-your-key")
```

## 抓取单个 URL

```python
from firecrawl import Firecrawl
from dotenv import load_dotenv
import os

load_dotenv()
firecrawl = Firecrawl(api_key=os.environ.get("FIRECRAWL_API_KEY"))

result = firecrawl.scrape(
    url="https://example.com",
    formats=["markdown", "html"]
)
print(result)
```

## 抓取选项

```python
result = firecrawl.scrape(
    url="https://example.com",
    formats=["markdown"],
    only_main_content=True,  # 只提取主要内容
    timeout=30  # 超时时间(秒)
)
```

## 返回结果结构

```python
{
    "success": True,
    "url": "https://example.com",
    "markdown": "# 标题...",  # 或 None
    "html": "<html>...</html>",  # 或 None
    "rawHtml": "<!DOCTYPE html>...",  # 或 None
    "metadata": {
        "title": "页面标题",
        "description": "页面描述",
        "language": "zh-CN",
        ...
    }
}
```

## 错误处理

```python
try:
    result = firecrawl.scrape(url, formats=["markdown"])
except Exception as e:
    print(f"抓取失败: {e}")
```
