# gh-kb Skill 设计文档

## 概述

gh-kb 是一个基于 GitHub CLI (`gh search`) 的知识搜索 skill，将 GitHub 作为技术新闻源和知识库使用。用户以自然语言提问，skill 智能分析意图，组合调用 gh search 的 5 种子命令（repos/issues/prs/commits/code），返回精炼的结构化结果列表。

## 设计方案：智能意图分析型（方案 B）

纯文档驱动，无额外脚本。SKILL.md 定义决策框架和工作流，Claude 利用推理能力做意图分析，直接通过 Bash 执行 gh CLI 命令。

## 文件结构

```
gh-kb/
├── SKILL.md                    # 核心：意图分析 + 搜索工作流 + 输出格式规范
└── references/
    └── gh-search-guide.md      # gh search 五种命令的完整参数参考
```

## 核心工作流（4 步）

### Step 1：意图分析

将用户自然语言问题分类：

| 意图类型 | 触发信号 | 主搜索命令 |
|---------|----------|-----------|
| 发现项目 | "有哪些"、"推荐"、"热门"、"最好的" | `gh search repos` |
| 追踪动态 | "最近"、"最新"、"进展"、"动态" | `gh search issues` + `gh search prs` |
| 学习实现 | "怎么实现"、"代码"、"用法"、"示例" | `gh search code` + `gh search repos` |
| 了解变更 | "更新了什么"、"changelog"、"发布" | `gh search commits` + `gh search prs` |
| 综合调研 | 复杂问题，需多维度信息 | 组合多个命令 |

### Step 2：构造搜索命令

根据意图类型智能选择：
- 搜索命令和关键词
- 过滤参数（语言、时间范围、star 数等）
- 排序方式（stars、updated、reactions 等）
- JSON 输出字段和 jq 表达式
- 结果数量限制（默认 10 条）

### Step 3：执行搜索

通过 Bash 工具执行 `gh search` 命令。对于组合搜索，尽可能并行执行多个命令。

### Step 4：汇总输出

标准化精炼列表格式（见输出格式规范）。

## 输出格式规范

### 仓库搜索结果
```
### [仓库名](url)
⭐ 12.3k | 🔀 1.2k | 📝 语言 | 🕐 最近更新时间
> 仓库描述
```

### Issues/PRs 搜索结果
```
### [标题](url)
📦 所属仓库 | 👤 作者 | 💬 评论数 | 🕐 创建/更新时间
> 正文摘要
```

### 代码搜索结果
```
### [文件路径](url)
📦 所属仓库 | 匹配片段预览
```

### 提交搜索结果
```
### [提交信息](url)
📦 所属仓库 | 👤 作者 | 🕐 提交时间
```

### 尾部固定附加
```
---
🔍 搜索条件：<实际执行的 gh search 命令摘要>
```

## 使用场景示例

1. "最近有哪些热门的 Rust Web 框架" → 发现项目 → `gh search repos`
2. "Go 语言 1.22 有什么重要更新" → 追踪动态 → `gh search issues` + `gh search commits`
3. "如何在 Python 中实现 retry 装饰器" → 学习实现 → `gh search code`
4. "React Server Components 最新进展" → 综合调研 → repos + issues + prs 组合
