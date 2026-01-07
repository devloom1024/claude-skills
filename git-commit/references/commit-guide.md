# Git Commit 规范指南

本文档基于阮一峰的 Commit Message 规范。

## Commit Message 格式

每个 commit message 包含三个部分：**Header**、**Body** 和 **Footer**。

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **Header 必需**，Body 和 Footer 可选
- 任何行不得超过 72-100 个字符

## Header 格式

Header 包含三个字段：`<type>(<scope>): <subject>`

### Type（必需）

标识 commit 的类别，只允许使用以下 7 个标识：

| Type | 说明 | 出现在 Change log |
|------|------|------------------|
| **feat** | 新功能（feature） | ✓ |
| **fix** | 修补 bug | ✓ |
| **docs** | 文档（documentation） | ✗ |
| **style** | 格式（不影响代码运行的变动，如空格、分号等） | ✗ |
| **refactor** | 重构（既不是新增功能，也不是修改 bug 的代码变动） | ✗ |
| **test** | 增加测试 | ✗ |
| **chore** | 构建过程或辅助工具的变动 | ✗ |

### Scope（可选）

用于说明 commit 影响的范围，比如：

- 数据层、控制层、视图层等
- 具体的模块名、组件名、文件名等
- 根据项目的实际情况而定

### Subject（必需）

commit 目的的简短描述，要求：

- **不超过 50 个字符**
- **以动词开头**，使用第一人称现在时，比如 change，而不是 changed 或 changes
- **第一个字母小写**
- **结尾不加句号**（.）

示例：
- ✓ `feat(user): add login functionality`
- ✓ `fix(api): resolve timeout issue in data fetch`
- ✗ `feat(user): Added login functionality` (应用过去时)
- ✗ `fix: Fix timeout issue.` (结尾不应有句号)

## Body（可选）

Body 部分是对本次 commit 的详细描述，可以分成多行。

要求：
- 使用第一人称现在时，比如使用 change 而不是 changed 或 changes
- 应该说明代码变动的**动机**，以及与以前行为的对比

示例：
```
More detailed explanatory text, if necessary.  Wrap it to
about 72 characters or so.

Further paragraphs come after blank lines.

- Bullet points are okay, too
- Use a hanging indent
```

## Footer（可选）

Footer 部分只用于两种情况：

### 1. 不兼容变动

如果当前代码与上一个版本不兼容，则 Footer 部分以 `BREAKING CHANGE` 开头，后面是对变动的描述、以及变动理由和迁移方法。

```
BREAKING CHANGE: isolate scope bindings definition has changed.

    To migrate the code follow the example below:

    Before:

    scope: {
      myAttr: 'attribute',
    }

    After:

    scope: {
      myAttr: '@',
    }
```

### 2. 关闭 Issue

如果当前 commit 针对某个 issue，那么可以在 Footer 部分关闭这个 issue。

```
Closes #234
```

也可以一次关闭多个 issue：

```
Closes #123, #245, #992
```

## 特殊类型：Revert

如果当前 commit 用于撤销以前的 commit，则必须以 `revert:` 开头，后面跟着被撤销 commit 的 Header。

Body 部分的格式是固定的，必须写成 `This reverts commit <hash>.`，其中的 hash 是被撤销 commit 的 SHA 标识符。

```
revert: feat(pencil): add 'graphiteWidth' option

This reverts commit 667ecc1654a317a13331b17617d973392f415f02.
```

## Type 选择指导

- **feat**: 添加新功能、新特性、新模块
- **fix**: 修复 bug、错误、异常
- **docs**: 仅修改文档，如 README、注释等
- **style**: 格式化代码，不改变代码逻辑（空格、缩进、分号等）
- **refactor**: 重构代码，既不修复 bug 也不添加新功能
- **test**: 添加或修改测试用例
- **chore**: 修改构建配置、依赖管理、CI/CD 等

## 示例

### 简单的 feat
```
feat(user): add email validation
```

### 带 scope 和 body 的 fix
```
fix(api): prevent race condition in data fetch

Add mutex lock to prevent concurrent requests from
accessing shared resource simultaneously.
```

### 带 footer 的 feat
```
feat(auth): implement JWT authentication

Add JWT token generation and validation middleware.

Closes #156
```

### 重大变更
```
feat(config): change config file format to YAML

BREAKING CHANGE: Configuration files must now be in YAML format.

To migrate, convert your config.json to config.yaml using the
provided migration script: npm run migrate-config
```
