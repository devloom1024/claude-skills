# {{project_name}} - AI 开发工作流

本项目使用 PIV Loop（Prime → Plan → Execute → Validate）AI 辅助开发流程。

## 目录结构

```
.agents/
├── plans/              # 功能实施计划
├── code-reviews/       # 代码审查结果
├── system-reviews/     # 系统审查报告
└── README.md           # 本文档
.claude/
├── commands/           # Slash 命令
├── reference/          # 最佳实践参考
└── CLAUDE.md           # 项目说明
```

## 可用命令

### PIV Loop 核心命令

| 命令 | 描述 |
|------|------|
| `/piv:prime` | 理解项目结构，输出项目概览 |
| `/piv:plan` | 创建详细实施计划 |
| `/piv:execute` | 按计划执行实现 |
| `/piv:validate` | 运行完整验证（lint + test + build） |
| `/piv:code-review` | 执行技术代码审查 |
| `/piv:system-review` | 分析计划与实现的偏差 |

### 配置命令

| 命令 | 描述 |
|------|------|
| `/piv:design` | 设计阶段：根据需求生成项目结构和规范框架 |
| `/piv:scan` | 扫描项目：检测技术栈，生成完整配置 |
| `/piv:sync` | 同步配置：重新检测并更新相关文件 |

### 辅助命令

| 命令 | 描述 |
|------|------|
| `/commit` | 创建规范化的 git commit |

## 工作流

```
需求 → /piv:prime    # 理解项目
     → /piv:plan     # 创建计划
     → /piv:execute  # 执行实现
     → /piv:validate # 验证质量
     → /commit       # 提交代码
```

## 添加新规范

如需为本项目添加额外的开发规范，按以下步骤操作：

### 1. 创建命令模板

在 `.claude/commands/` 下创建新目录：

```bash
mkdir -p .claude/commands/my-feature
```

创建 `my-feature/describe.md`：

```markdown
---
description: [命令描述]
argument-hint: [参数提示]
---

# [命令名称]

## 执行步骤

1. [步骤1]
2. [步骤2]

## 输出

[期望输出格式]
```

### 2. 创建参考文档

在 `.claude/reference/` 下创建规范文档：

```markdown
# [规范名称]

## 适用范围
[何时使用此规范]

## 规则

### 规则 1
[描述]

### 规则 2
[描述]

## 示例

```[language]
// 正确示例
code here

// 错误示例
code here
```
```

### 3. 更新本文件

在下方「项目特定命令」或「项目规范」部分添加说明。

---

## 项目特定命令

（本区域由项目维护者填写）

### 待添加

---

## 项目规范

（本区域由项目维护者填写）

### 代码风格

- 命名约定：`snake_case` / `camelCase` / `kebab-case`
- 缩进：空格数
- 最大行长度：字符数

### 文档规范

- 所有公开 API 需要文档字符串
- README 需包含：安装、用法、测试
- CHANGELOG 使用 [Keep a Changelog](https://keepachangelog.com/) 格式

### 测试规范

- 单元测试覆盖率目标：%
- 集成测试位于：`tests/integration/`
- Mock 策略：[说明]

### 提交规范

- 使用 [Conventional Commits](https://www.conventionalcommits.org/)
- 类型：feat、fix、docs、style、refactor、test、chore
- 最大提交粒度：[说明]

---

## 常见问题

### Q：命令不显示怎么办？

A：重新加载 Claude Code 窗口（Cmd+Shift+P：Reload Window）

### Q：如何修改检测到的项目配置？

A：在项目根目录创建 `piv-config.json` 覆盖自动检测

### Q：如何跳过某些参考文档？

A：在 `piv-config.json` 中设置 `skip_reference`
