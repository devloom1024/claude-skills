# gh search 命令参考

## 目录

- [通用选项](#通用选项)
- [数值和日期过滤语法](#数值和日期过滤语法)
- [gh search repos](#gh-search-repos)
- [gh search issues](#gh-search-issues)
- [gh search prs](#gh-search-prs)
- [gh search commits](#gh-search-commits)
- [gh search code](#gh-search-code)
- [常用 jq 表达式](#常用-jq-表达式)

## 通用选项

所有子命令均支持：

| 参数 | 说明 |
|------|------|
| `--json <fields>` | JSON 格式输出指定字段（逗号分隔） |
| `-q, --jq <expr>` | jq 表达式过滤 JSON 输出 |
| `-t, --template <string>` | Go 模板格式化输出 |
| `-w, --web` | 浏览器打开搜索结果 |
| `-L, --limit <int>` | 最大结果数（默认 30） |

## 数值和日期过滤语法

数值：`>100`、`>=100`、`<100`、`<=100`、`100..200`

日期：`>2024-01-01`、`>=2024-01-01`、`2024-01-01..2024-12-31`

## gh search repos

搜索仓库。

**关键参数：**

| 参数 | 说明 |
|------|------|
| `--language <string>` | 编程语言 |
| `--stars <number>` | Star 数量 |
| `--forks <number>` | Fork 数量 |
| `--owner <strings>` | 仓库所有者 |
| `--topic <strings>` | 话题标签 |
| `--created <date>` | 创建日期 |
| `--updated <date>` | 最后更新日期 |
| `--license <strings>` | 许可证类型 |
| `--match <strings>` | 搜索范围：`name`、`description`、`readme` |
| `--archived` | 是否已归档 |
| `--size <string>` | 仓库大小（KB） |
| `--followers <number>` | 关注者数 |
| `--visibility <strings>` | `public`/`private`/`internal` |

**排序（`--sort`）：** `forks`、`help-wanted-issues`、`stars`、`updated`（默认 `best-match`）

**JSON 字段：** `fullName`、`description`、`stargazersCount`、`forksCount`、`language`、`updatedAt`、`createdAt`、`url`、`homepage`、`license`、`owner`、`isArchived`、`openIssuesCount`、`watchersCount`、`defaultBranch`、`size`、`visibility`

## gh search issues

搜索 Issues。

**关键参数：**

| 参数 | 说明 |
|------|------|
| `-R, --repo <strings>` | 仓库 |
| `--owner <strings>` | 仓库所有者 |
| `--author <string>` | 作者 |
| `--assignee <string>` | 指派人 |
| `--label <strings>` | 标签 |
| `--state <string>` | `open`/`closed` |
| `--language <string>` | 编程语言 |
| `--created <date>` | 创建日期 |
| `--updated <date>` | 更新日期 |
| `--closed <date>` | 关闭日期 |
| `--comments <number>` | 评论数 |
| `--reactions <number>` | 反应数 |
| `--interactions <number>` | 互动数 |
| `--match <strings>` | 搜索范围：`title`、`body`、`comments` |
| `--involves <user>` | 参与者 |
| `--mentions <user>` | 提及的用户 |
| `--milestone <title>` | 里程碑 |

**排序（`--sort`）：** `comments`、`created`、`interactions`、`reactions`、`reactions-+1`、`reactions--1`、`reactions-heart`、`reactions-smile`、`reactions-tada`、`reactions-thinking_face`、`updated`

**JSON 字段：** `title`、`url`、`state`、`author`、`labels`、`assignees`、`body`、`commentsCount`、`createdAt`、`updatedAt`、`closedAt`、`repository`、`number`、`isLocked`、`isPullRequest`

## gh search prs

搜索 Pull Requests。继承 issues 的大部分参数，另有：

**额外参数：**

| 参数 | 说明 |
|------|------|
| `-B, --base <string>` | 目标分支 |
| `-H, --head <string>` | 源分支 |
| `--draft` | 是否草稿 |
| `--merged` | 是否已合并 |
| `--merged-at <date>` | 合并日期 |
| `--checks <string>` | CI 状态：`pending`/`success`/`failure` |
| `--review <string>` | 审查状态：`none`/`required`/`approved`/`changes_requested` |
| `--review-requested <user>` | 请求审查的用户 |
| `--reviewed-by <user>` | 审查者 |

**排序：** 同 issues

**JSON 字段：** 同 issues，另加 `isDraft`

## gh search commits

搜索提交。

**关键参数：**

| 参数 | 说明 |
|------|------|
| `-R, --repo <strings>` | 仓库 |
| `--owner <strings>` | 仓库所有者 |
| `--author <string>` | 作者 |
| `--author-date <date>` | 作者日期 |
| `--author-email <string>` | 作者邮箱 |
| `--committer <string>` | 提交者 |
| `--committer-date <date>` | 提交日期 |
| `--merge` | 是否合并提交 |
| `--hash <string>` | 提交哈希 |

**排序（`--sort`）：** `author-date`、`committer-date`

**JSON 字段：** `sha`、`commit`、`author`、`committer`、`url`、`repository`、`parents`

## gh search code

搜索代码。**注意：查询关键词为必填项。**

**关键参数：**

| 参数 | 说明 |
|------|------|
| `-R, --repo <strings>` | 仓库 |
| `--owner <strings>` | 仓库所有者 |
| `--language <string>` | 编程语言 |
| `--filename <string>` | 文件名 |
| `--extension <string>` | 文件扩展名 |
| `--size <string>` | 文件大小（字节） |
| `--match <strings>` | 搜索范围：`file`、`path` |

**排序：** 仅支持 best-match，无 `--sort` 参数

**JSON 字段：** `path`、`repository`、`sha`、`textMatches`、`url`

## 常用 jq 表达式

```bash
# repos: 名称 + stars + 描述
--jq '.[] | "⭐\(.stargazersCount) \(.fullName): \(.description)"'

# issues: 标题 + 仓库 + 评论数
--jq '.[] | "💬\(.commentsCount) [\(.repository.nameWithOwner)] \(.title)"'

# code: 文件路径 + 仓库
--jq '.[] | "📄 \(.repository.fullName)/\(.path)"'

# commits: 消息 + 作者
--jq '.[] | "🔨 \(.commit.author.name): \(.commit.message | split("\n")[0])"'

# 仅提取 URL 列表
--jq '.[].url'

# 提取前 N 条结果的特定字段
--jq '[.[:5] | .[] | {name: .fullName, stars: .stargazersCount}]'
```

---

## 搜索策略模式

### 扩展策略（搜索结果过少时）

结果为空或过少时，通过多角度搜索扩大范围。很多项目是多平台通用的，名称/描述中可能不包含目标关键词。

#### 三层关键词扩展

逐层扩大搜索范围：

```bash
# 第一层：直接关键词
gh search repos "react state management" --sort stars

# 第二层：生态关联词（同类工具，很多项目同时支持多个）
gh search repos "redux alternative" --sort stars
gh search repos "zustand vs jotai" --sort stars

# 第三层：通用概念词（不含具体工具名的通用项目）
gh search repos "frontend state library" --sort stars
gh search repos "reactive store javascript" --sort stars
```

#### 资源列表发现法

先找 awesome 列表等资源汇总，从中发现热门项目：

```bash
gh search repos "awesome-react-state" --sort stars
gh search repos "awesome-state-management" --sort stars
# 从列表中发现热门项目，再针对性搜索
```

#### 组织名/品牌名搜索

部分热门项目使用独立品牌名，直接搜索关键词会遗漏：

```bash
# 搜索特定组织的项目
gh search repos --owner "pmndrs" --sort stars

# 搜索品牌名（如 zustand、jotai 等独立品牌）
gh search repos "zustand" --sort stars
```

#### 多关键词并行搜索

多个相关关键词同时搜索，取并集：

```bash
# 并行执行（通过 Claude 的并行 Bash 调用）
gh search repos "rust web framework" --sort stars
gh search repos "rust http server" --sort stars
gh search repos "rust async web" --sort stars
```

### 精选策略（搜索结果过多时）

结果过多或需要精选时，通过过滤条件收窄范围。

#### 时间范围过滤

```bash
# 最近创建的项目（发现新兴工具）
gh search repos "rust web" --created ">2025-01-01" --sort stars

# 最近更新的项目（发现活跃维护的工具）
gh search repos "rust web" --updated ">2025-06-01" --sort updated
```

#### Star 数分级搜索

```bash
# 顶级项目（成熟稳定）
gh search repos "rust web" --stars ">1000" --sort stars

# 中等项目（活跃发展中）
gh search repos "rust web" --stars "100..1000" --sort updated

# 新兴项目（早期但有潜力）
gh search repos "rust web" --stars "<100" --created ">2025-01-01" --sort created
```
