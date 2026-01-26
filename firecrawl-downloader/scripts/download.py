#!/usr/bin/env python3
"""
Firecrawl Downloader - 将网页内容抓取并保存为指定格式

用法:
    python download.py <url> <output_dir> <format> [--api-key KEY] [--filename NAME]

参数:
    url: 要抓取的网页 URL
    output_dir: 输出目录
    format: 输出格式 (markdown, html, rawHtml)
    --api-key: Firecrawl API Key (可选，从环境变量或 .env 文件读取)
    --filename: 自定义输出文件名 (可选，默认从 URL 生成)

支持格式:
    - markdown: 纯文本 markdown
    - html: 格式化的 HTML
    - rawHtml: 原始 HTML
"""

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("请安装 dotenv: pip install python-dotenv")
    sys.exit(1)

try:
    from firecrawl import Firecrawl
except ImportError:
    print("请安装 firecrawl-py: pip install firecrawl-py")
    sys.exit(1)


def load_api_key() -> str:
    """从环境变量或 .env 文件加载 API Key"""
    # 先尝试环境变量
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if api_key:
        return api_key

    # 尝试从 .env 文件加载
    load_dotenv()
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if api_key:
        return api_key

    # 尝试常见位置的 .env 文件
    env_paths = [
        Path(".env"),
        Path("~/.env").expanduser(),
        Path("~/.firecrawl.env").expanduser(),
        Path("~/.claude/.env").expanduser(),
    ]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            api_key = os.environ.get("FIRECRAWL_API_KEY")
            if api_key:
                return api_key

    return ""


def validate_format(format_str: str) -> list[str]:
    """验证并规范化格式参数"""
    valid_formats = {"markdown", "html", "rawHtml"}
    formats = [f.strip().lower() for f in format_str.split(",")]

    invalid = [f for f in formats if f not in valid_formats]
    if invalid:
        print(f"警告: 无效的格式 {invalid}，已忽略")
        formats = [f for f in formats if f in valid_formats]

    if not formats:
        print("错误: 至少需要指定一个有效格式 (markdown, html, rawHtml)")
        sys.exit(1)

    return formats


def download(url: str, output_dir: str, format_str: str, api_key: str = None, filename: str = None) -> dict:
    """
    使用 Firecrawl 抓取网页内容

    参数:
        url: 要抓取的网页 URL
        output_dir: 输出目录
        format_str: 输出格式，逗号分隔
        api_key: Firecrawl API Key
        filename: 自定义文件名 (可选，默认从 URL 生成)

    返回:
        包含结果的字典
    """
    # 加载 API Key
    if not api_key:
        api_key = load_api_key()

    if not api_key:
        print("错误: 未找到 Firecrawl API Key")
        print("请通过以下方式设置:")
        print("  1. 环境变量: export FIRECRAWL_API_KEY=fc-xxx")
        print("  2. .env 文件: 添加 FIRECRAWL_API_KEY=fc-xxx")
        print("  3. 命令行参数: --api-key fc-xxx")
        sys.exit(1)

    # 初始化客户端
    firecrawl = Firecrawl(api_key=api_key)

    # 验证格式
    formats = validate_format(format_str)

    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 抓取网页
    print(f"正在抓取: {url}")
    print(f"格式: {', '.join(formats)}")
    print(f"输出目录: {output_path}")

    try:
        result = firecrawl.scrape(url, formats=formats)

        # 保存结果
        saved_files = []
        # 使用自定义文件名或从 URL 生成
        base_filename = filename if filename else url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")

        # 处理 Pydantic Document 对象
        markdown_content = result.markdown if hasattr(result, 'markdown') else None
        html_content = result.html if hasattr(result, 'html') else None
        raw_html_content = result.raw_html if hasattr(result, 'raw_html') else None
        metadata = result.metadata_dict if hasattr(result, 'metadata_dict') else {}

        if "markdown" in formats and markdown_content:
            md_path = output_path / f"{base_filename}.md"
            md_path.write_text(markdown_content, encoding="utf-8")
            saved_files.append(str(md_path))
            print(f"已保存 Markdown: {md_path}")

        if "html" in formats and html_content:
            html_path = output_path / f"{base_filename}.html"
            html_path.write_text(html_content, encoding="utf-8")
            saved_files.append(str(html_path))
            print(f"已保存 HTML: {html_path}")

        if "rawHtml" in formats and raw_html_content:
            raw_path = output_path / f"{base_filename}_raw.html"
            raw_path.write_text(raw_html_content, encoding="utf-8")
            saved_files.append(str(raw_path))
            print(f"已保存 Raw HTML: {raw_path}")

        return {
            "success": True,
            "url": url,
            "saved_files": saved_files,
            "metadata": metadata
        }

    except Exception as e:
        print(f"抓取失败: {e}")
        return {
            "success": False,
            "url": url,
            "error": str(e)
        }


def main():
    """命令行入口"""
    if len(sys.argv) < 4:
        print(__doc__)
        print("\n示例:")
        print(f"  {sys.argv[0]} https://example.com ./output markdown")
        print(f"  {sys.argv[0]} https://example.com ./output html --api-key fc-xxx")
        print(f"  {sys.argv[0]} https://example.com ./output markdown --filename mydoc")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2]
    format_str = sys.argv[3]

    # 解析可选参数
    api_key = None
    filename = None
    for i, arg in enumerate(sys.argv[4:], start=4):
        if arg == "--api-key" and i + 1 < len(sys.argv):
            api_key = sys.argv[i + 1]
        elif arg == "--filename" and i + 1 < len(sys.argv):
            filename = sys.argv[i + 1]

    result = download(url, output_dir, format_str, api_key, filename)

    if result["success"]:
        print("\n抓取完成!")
        print(f"保存的文件: {', '.join(result['saved_files'])}")
        sys.exit(0)
    else:
        print(f"\n抓取失败: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
