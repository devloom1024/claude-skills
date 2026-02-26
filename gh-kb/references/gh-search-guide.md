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
