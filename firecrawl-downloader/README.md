# Firecrawl Downloader

使用 Firecrawl Python SDK 将网页内容下载为 Markdown、HTML 或原始 HTML 格式。

## 功能特点

- 支持多种输出格式：Markdown、HTML、RawHTML
- 支持从 .env 文件读取 API Key
- 简单的命令行接口
- Python API 供程序调用

## 并发限制

**不推荐使用并发下载**，Firecrawl API 有速率限制。如需并发，最多 3 个并行请求，并设置适当的延迟。

## 安装

```bash
pip install -r requirements.txt
```

## 配置 API Key

### 方法一：使用 .env 文件

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
```

### 方法二：环境变量

```bash
export FIRECRAWL_API_KEY=fc-your-api-key
```

### 方法三：命令行参数

```bash
python scripts/download.py <url> <output_dir> <format> --api-key fc-your-key --filename myfile
```

## 使用方法

### 命令行

```bash
python scripts/download.py <url> <output_dir> <format> [--api-key KEY] [--filename NAME]
```

#### 参数说明

| 参数 | 说明 |
|------|------|
| url | 要抓取的网页 URL (必需) |
| output_dir | 输出目录 (必需) |
| format | 输出格式: `markdown`, `html`, `rawHtml` (必需) |
| --api-key | Firecrawl API Key (可选) |
| --filename | 自定义输出文件名 (可选，默认从 URL 生成) |

#### 示例

```bash
# 下载为 Markdown 格式
python scripts/download.py https://example.com ./output markdown

# 下载为 HTML 格式
python scripts/download.py https://example.com ./output html

# 下载多种格式 (逗号分隔)
python scripts/download.py https://example.com ./output markdown,html

# 指定 API Key
python scripts/download.py https://example.com ./output markdown --api-key fc-xxx

# 自定义输出文件名
python scripts/download.py https://example.com ./output markdown --filename mydoc
```

### Python API

```python
import sys
sys.path.insert(0, 'scripts')
from download import download

# 抓取网页
result = download(
    url="https://example.com",
    output_dir="./output",
    format_str="markdown,html",
    filename="mydoc"  # 可选，自定义文件名
)

if result["success"]:
    print("保存的文件:", result["saved_files"])
    print("元数据:", result["metadata"])
else:
    print("抓取失败:", result["error"])
```

## 输出格式

| 格式 | 说明 | 文件扩展名 |
|------|------|-----------|
| markdown | 纯文本 Markdown 格式 | .md |
| html | 格式化后的 HTML | .html |
| rawHtml | 原始 HTML 内容 | _raw.html |

## 获取 API Key

1. 访问 [firecrawl.dev](https://firecrawl.dev)
2. 注册账号并获取 API Key
3. 免费套餐包含一定数量的抓取请求

## 项目结构

```
firecrawl-downloader/
├── SKILL.md              # Skill 定义文件
├── README.md             # 本文档
├── requirements.txt      # Python 依赖
├── .env.example          # .env 配置示例
├── scripts/
│   └── download.py       # 核心下载脚本
└── REFERENCES.md         # SDK 参考文档
```

## 依赖

- `firecrawl-py` - Firecrawl Python SDK
- `python-dotenv` - .env 文件支持

## 故障排除

### 错误: 未找到 API Key

确保已正确配置 API Key：
```bash
# 检查环境变量
echo $FIRECRAWL_API_KEY

# 或确认 .env 文件存在且内容正确
cat .env
```

### 错误: 抓取失败

- 检查 URL 是否可访问
- 确认 API Key 有效且未超出配额
- 尝试添加 `--api-key` 参数直接指定

## License

MIT
