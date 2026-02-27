---
name: gh-kb
description: |
  基于 GitHub CLI (gh search) 的知识搜索工具，将 GitHub 作为技术新闻源和知识库。支持搜索仓库、Issues、PRs、提交和代码。

  使用场景：
  (1) 用户想发现某个领域/技术的优质项目或工具
  (2) 用户想追踪某个项目或技术的最新动态和进展
  (3) 用户想学习某个功能的代码实现或用法示例
  (4) 用户想了解某个项目的最近变更或发布
  (5) 用户需要综合调研某个技术话题
  (6) 用户说"搜索"、"有哪些"、"最近"、"热门"、"推荐"等关键词并涉及 GitHub 生态

  不要在以下情况使用：
  - 用户询问的内容与 GitHub/技术生态无关
  - 用户只是想操作本地 git 仓库（非搜索）
  - 用户已经提供了明确的 URL，不需要搜索
---

# gh-kb: GitHub 知识搜索

前置条件：需要已安装并登录 `gh` CLI。

## 工作流

```
环境检测 → 用户提问 → 意图分析 → 构造命令 → 执行搜索 → 汇总输出
```

### Step 0：环境检测

在执行搜索前，先检测 `gh` 是否可用：

1. 运行 `gh --version`，若失败则告知用户安装地址 https://github.com/cli/cli#installation ，终止流程
2. 运行 `gh auth status`，若未登录则提示执行 `gh auth login`，终止流程

### Step 1：意图分析

根据用户问题判断搜索意图，选择对应的搜索策略：

| 意图 | 触发信号 | 搜索命令 |
|------|----------|---------|
| 发现项目 | "有哪些"、"推荐"、"热门"、"最好的"、"工具"、"框架"、"库" | `gh search repos` |
| 追踪动态 | "最近"、"最新"、"进展"、"动态"、"更新" | `gh search issues` + `gh search prs` |
| 学习实现 | "怎么实现"、"代码"、"用法"、"示例"、"如何" | `gh search code` + `gh search repos` |
| 了解变更 | "更新了什么"、"changelog"、"发布"、"release" | `gh search commits` + `gh search prs` |
| 综合调研 | 复杂问题或多维度信息需求 | 组合多个命令 |

一个问题可能触发多个搜索命令（多源组合搜索），根据需要灵活组合。

### Step 2：构造命令

根据意图决定：

1. **搜索命令**：选择 repos/issues/prs/commits/code 中的一个或多个
2. **关键词**：从用户问题中提取核心搜索词，翻译为英文效果更好
3. **过滤参数**：语言（`--language`）、时间范围（`--created`/`--updated`）、star 数（`--stars`）等
4. **排序**：stars（热度）、updated（时效）、reactions（关注度）、comments（讨论度）
5. **输出字段**：始终使用 `--json` 指定需要的字段
6. **数量**：默认 `--limit 10`，可根据需要调整

构造命令时参考 [references/gh-search-guide.md](references/gh-search-guide.md) 获取完整的参数和 JSON 字段列表。

**关键词策略：**
- 用户中文问题应翻译为英文关键词搜索
- 使用引号包裹精确短语（如 `"server components"`）
- 使用 `--` 分隔排除语法（如 `-- -label:wontfix`）

### Step 3：执行搜索

通过 Bash 工具执行 `gh search` 命令：
- 多个搜索命令应**并行执行**以提高效率
- 始终使用 `--json` + 需要的字段，获取结构化数据
- 可选配合 `--jq` 做初步过滤

**命令示例：**

```bash
# 发现项目
gh search repos "rust web framework" --language rust --sort stars --limit 10 \
  --json fullName,stargazersCount,forksCount,description,language,updatedAt,url

# 追踪动态
gh search issues "server components" --repo facebook/react --sort reactions --limit 10 \
  --json title,url,state,author,commentsCount,createdAt,updatedAt,repository

# 学习实现
gh search code "def retry" --language python --limit 10 \
  --json path,repository,url,textMatches

# 了解变更
gh search commits "v2.0" --repo vercel/next.js --limit 10 \
  --json sha,commit,author,url,repository

# 搜索 PRs
gh search prs "performance" --repo golang/go --sort reactions --state open --limit 10 \
  --json title,url,author,commentsCount,createdAt,repository,state
```

### Step 4：汇总输出

将 JSON 结果整理为精炼列表。根据搜索类型使用对应格式：

**仓库：**
```
### [fullName](url)
⭐ stargazersCount | 🔀 forksCount | 📝 language | 🕐 updatedAt
> description
```

**Issues / PRs：**
```
### [title](url)
📦 repository | 👤 author | 💬 commentsCount | 🕐 createdAt
> body 摘要（首 100 字，如有）
```

**代码：**
```
### [path](url)
📦 repository
> textMatches 匹配片段预览
```

**提交：**
```
### [commit.message 首行](url)
📦 repository | 👤 author | 🕐 日期
```

**尾部固定附加搜索条件摘要：**
```
---
🔍 搜索条件：<实际执行的 gh search 命令>
```
## 注意事项

- `gh search code` 的查询关键词为必填项，不能为空
- GitHub 搜索 API 有速率限制，避免短时间内大量查询
- 代码搜索使用旧版引擎，结果可能与 github.com 网页端不完全一致
- Star 数等数值字段可用范围表达式：`>1000`、`100..500`
- 日期字段可用范围表达式：`>2024-01-01`、`2024-01-01..2024-12-31`
- **搜索结果过少时**：参考 [references/gh-search-guide.md](references/gh-search-guide.md) 中的「扩展策略」，使用关键词扩展、资源列表发现、品牌名搜索等方式扩大范围
- **搜索结果过多时**：参考同文件中的「精选策略」，使用时间范围过滤、Star 数分级等方式收窄范围
