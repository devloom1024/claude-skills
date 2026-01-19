---
name: git-commit
description: |
  智能生成符合规范的 Git Commit Message。基于阮一峰的 Commit 规范（Angular 规范），自动分析代码变更并生成结构化的提交信息。

  使用场景：
  (1) 用户要求创建 git commit 或提交代码时
  (2) 用户说"提交"、"commit"、"提交代码"等关键词
  (3) 用户要求生成 commit message
  (4) 用户希望使用规范化的提交信息

  不要在以下情况使用：
  - 用户明确指定了完整的 commit message
  - 用户只是询问 git commit 的使用方法（信息查询，非执行操作）
---

# Git Commit 智能提交

自动分析代码变更，生成符合阮一峰规范的 Git Commit Message，并执行提交操作。

## 工作流程

### 1. 分析代码变更

首先并行执行以下命令：

```bash
git status
git diff --cached
git diff
git log --oneline -10
```

- `git status` - 查看暂存和未暂存的文件
- `git diff --cached` - 查看已暂存的更改
- `git diff` - 查看未暂存的更改
- `git log --oneline -10` - 查看最近 10 条提交记录，用于推断项目使用的语言

### 2. 智能推断语言

分析最近 10 条 commit message，统计中英文使用比例：
- 如果中文占比超过 50% → 使用中文生成 commit message
- 如果英文占比超过 50% → 使用英文生成 commit message
- 如果无法判断（无历史记录）→ 默认使用英文

### 3. 智能推断 Type

基于代码变更自动判断 commit type：

- **feat** - 新增文件、新增函数/类/方法、新增功能模块
- **fix** - 修复 bug、异常处理、错误修正
- **docs** - 仅修改 README、注释、文档文件
- **style** - 格式化、缩进调整、添加分号等（不改变逻辑）
- **refactor** - 重构代码、重命名变量/函数、优化代码结构
- **test** - 添加或修改测试文件、测试用例
- **chore** - 修改配置文件、依赖更新、构建脚本

**判断优先级**：
1. 如果有 bug 修复 → `fix`
2. 如果有新功能 → `feat`
3. 如果只改文档 → `docs`
4. 如果是测试相关 → `test`
5. 如果是重构 → `refactor`
6. 如果是格式调整 → `style`
7. 其他配置变更 → `chore`

### 3. 确定 Scope（可选）

根据变更的文件路径推断 scope：

- 单个模块/组件 → 使用该模块名
- 多个相关模块 → 使用上层模块名
- 跨多个不相关模块 → 省略 scope

示例：
- `src/auth/login.ts` → `scope: auth`
- `src/components/Button.tsx` → `scope: button`
- 多个不相关文件 → 不设置 scope

### 4. 生成 Subject

生成简短的描述（不超过 50 个字符）：

**规则**：
- 使用动词开头（add, fix, update, remove, refactor 等）
- 第一人称现在时
- 首字母小写
- 不加句号
- 描述做了什么，而不是为什么

**示例**：
- ✓ `add user authentication`
- ✓ `fix memory leak in event handler`
- ✓ `update API endpoint path`
- ✗ `Added user authentication` (过去时)
- ✗ `Fix memory leak.` (有句号)

### 5. 生成完整的 Commit Message

基本格式：

```
<type>(<scope>): <subject>
```

如果变更较大或需要说明动机，添加 body：

```
<type>(<scope>): <subject>

<body>
```

如果有关闭的 issue，添加 footer：

```
<type>(<scope>): <subject>

<body>

Closes #123
```

### 6. 暂存文件并提交

将所有未暂存的文件添加到暂存区：

```bash
git add .
```

执行提交：

```bash
git commit -m "<message>"
```

对于包含 body 和 footer 的多行 message，使用 heredoc：

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

<footer>
EOF
)"
```

### 7. 确认提交成功

提交后运行：

```bash
git status
git log -1 --oneline
```

向用户展示提交结果。

## 详细规范参考

如需查看完整的规范说明、示例和特殊情况处理，阅读 [references/commit-guide.md](references/commit-guide.md)。

## 示例场景

### 场景 1：新增功能
```
用户：帮我提交代码
[分析后发现新增了登录功能]
→ feat(auth): add user login functionality
```

### 场景 2：修复 Bug
```
用户：commit 一下
[分析后发现修复了内存泄漏]
→ fix(event): resolve memory leak in event handler
```

### 场景 3：重构代码
```
用户：提交这些改动
[分析后发现重构了数据层]
→ refactor(data): simplify database query logic
```

### 场景 4：多行 message
```
用户：提交代码并关闭 issue #156
[分析后发现实现了 JWT 认证]
→ feat(auth): implement JWT authentication

Add JWT token generation and validation middleware
for secure API access.

Closes #156
```

## 注意事项

1. **仔细分析变更**：不要仅根据文件名判断，需要查看具体的代码变更内容
2. **type 选择准确**：确保 type 反映变更的真实性质
3. **subject 简洁明确**：控制在 50 字符内，清晰描述做了什么
4. **语言自动推断**：根据历史 commit message 自动判断使用中文或英文，无需用户指定
5. **询问用户确认**：生成 message 后，向用户展示并询问是否确认提交

## 工作流程总结

```
1. 执行 git status + git diff + git log (并行)
   ↓
2. 分析变更内容
   ↓
3. 推断语言（根据历史 commit）
   ↓
4. 推断 type 和 scope
   ↓
5. 生成 subject
   ↓
6. 展示给用户确认
   ↓
7. 执行 git add .
   ↓
8. 执行 git commit
   ↓
9. 确认成功并展示结果
```
