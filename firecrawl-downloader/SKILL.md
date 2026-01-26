---
name: firecrawl-downloader
description: 使用 Firecrawl Python SDK 将网页内容抓取并保存为指定格式。支持从 .env 文件读取 API Key，适用于下载文档、归档网页、提取内容等场景。
---

# Firecrawl Downloader

使用 Firecrawl API 将网页内容下载为 Markdown、HTML 或原始 HTML 格式。

## 使用场景

当用户需要：
- 将网页内容保存为离线文档
- 抓取网站内容用于分析或归档
- 提取网页的 Markdown 或 HTML 格式
- 从 .env 文件配置 API Key

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API Key (三选一)
export FIRECRAWL_API_KEY=fc-your-key     # 环境变量
echo "FIRECRAWL_API_KEY=fc-your-key" > .env  # .env 文件
python scripts/download.py <url> <output_dir> <format> --api-key fc-your-key  # 命令行参数
```

## 命令行用法

```bash
python scripts/download.py <url> <output_dir> <format> [--api-key KEY] [--filename NAME]
```

### 参数

| 参数 | 说明 |
|------|------|
| url | 要抓取的网页 URL |
| output_dir | 输出目录 |
| format | 格式: `markdown`, `html`, `rawHtml` (可逗号分隔) |
| --api-key | API Key (可选) |
| --filename | 自定义输出文件名 (可选) |

### 示例

```bash
# 下载为 Markdown
python scripts/download.py https://example.com ./output markdown

# 下载为 HTML
python scripts/download.py https://example.com ./output html

# 下载多种格式
python scripts/download.py https://example.com ./output markdown,html

# 指定 API Key
python scripts/download.py https://example.com ./output markdown --api-key fc-xxx

# 自定义输出文件名
python scripts/download.py https://example.com ./output markdown --filename mydoc
```

## Python API

```python
from scripts.download import download

result = download(
    url="https://example.com",
    output_dir="./output",
    format_str="markdown,html",
    filename="mydoc"  # 可选，自定义文件名
)

if result["success"]:
    print(f"保存的文件: {result['saved_files']}")
```

## API Key 配置

按优先级查找以下位置：
1. `--api-key` 命令行参数
2. `FIRECRAWL_API_KEY` 环境变量
3. `.env` 文件中的 `FIRECRAWL_API_KEY`
4. `~/.env` 文件
5. `~/.firecrawl.env` 文件

## 依赖

- `firecrawl-py` - Firecrawl Python SDK
- `python-dotenv` - .env 文件支持

参考 [REFERENCES.md](REFERENCES.md) 了解更多 Firecrawl SDK 用法。
