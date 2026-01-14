---
description: 扫描已有项目：检测技术栈，生成完整配置
argument-hint: none
---

# /piv:scan：扫描项目并生成配置

## 执行步骤

### 第一步：扫描项目结构

```bash
# 列出项目文件
git ls-files

# 查找配置文件
find . -maxdepth 3 -type f \( -name "package.json" -o -name "pyproject.toml" -o -name "pom.xml" -o -name "go.mod" -o -name "Cargo.toml" \) 2>/dev/null

# 查找测试配置
find . -maxdepth 2 -type f \( -name "pytest.ini" -o -name "vitest.config.*" -o -name "jest.config.*" -o -name ".eslintrc.*" -o -name "ruff.toml" \) 2>/dev/null
```

### 第二步：检测技术栈

根据扫描结果确定：

| 检测项 | 识别依据 | 示例 |
|--------|----------|------|
| 语言 | 文件扩展名、配置文件 | Python、TypeScript、Go、Rust |
| 框架 | 依赖项、目录结构 | FastAPI、React、Spring、Django |
| 包管理器 | lock 文件 | uv、npm、pnpm、maven、cargo |
| 测试框架 | 配置文件、依赖 | pytest、vitest、jest、go test |
| 代码规范 | 配置文件 | ruff、eslint、prettier、golint |

### 第三步：生成命令文件

根据检测结果，用中文生成以下命令文件：

#### 3.1 创建 PIV Loop 核心命令

**`.claude/commands/core_piv_loop/prime.md`**

```markdown
# /piv:prime：理解项目结构

## 执行步骤

1. 列出项目文件
2. 阅读 CLAUDE.md 和 README.md
3. 识别入口文件和配置
4. 检查最近 git 活动

## 输出：项目概览报告
- 技术栈
- 关键文件
- 代码规范
- 当前状态
```

**`.claude/commands/core_piv_loop/plan.md`**

```markdown
# /piv:plan：创建实施计划

## 输入

功能描述：`$ARGUMENTS`

## 执行步骤

1. 理解需求
2. 分析代码库
3. 研究最佳实践
4. 创建详细计划

## 计划结构
- 功能描述
- 用户故事
- 上下文引用
- 实施阶段
- 步骤化任务
- 测试策略
- 验证命令
```

**`.claude/commands/core_piv_loop/execute.md`**

```markdown
# /piv:execute：执行实施计划

## 输入

计划文件路径：`$ARGUMENTS`

## 执行步骤

1. 阅读并理解计划
2. 按顺序执行任务
3. 实现测试策略
4. 运行验证命令

## 验证清单
- [ ] 所有任务完成
- [ ] 测试通过
- [ ] Lint 通过
- [ ] 可提交代码
```

#### 3.2 创建验证命令

**`.claude/commands/validation/validate.md`**

```markdown
# /piv:validate：运行完整验证

## 验证层级

1. Lint：`[lint命令]`
2. 测试：`[test命令]`
3. 构建：`[build命令]`

## 输出

验证结果汇总
```

#### 3.3 创建提交命令

**`.claude/commands/commit.md`**

```markdown
# /commit：创建提交

1. 查看变更：`git status && git diff`
2. 添加变更：`git add .`
3. 创建提交（遵循 Conventional Commits）
```

### 第四步：生成参考文档

根据技术栈选择生成：

| 语言 | 参考文档 |
|------|----------|
| Python | `fastapi-best-practices.md`、`sqlite-best-practices.md`、`testing-and-logging.md` |
| TypeScript | `react-best-practices.md`、`testing-and-logging.md` |
| Java | `spring-best-practices.md`、`testing-and-logging.md` |
| Go | `go-best-practices.md`、`testing-and-logging.md` |

### 第五步：更新 .agents/README.md

更新 `.agents/README.md`，包含：

- 项目技术栈说明
- 可用命令列表
- 验证命令
- 新增规范指南

## 输出

1. `.claude/commands/core_piv_loop/*.md`
2. `.claude/commands/validation/validate.md`
3. `.claude/commands/commit.md`
4. `.claude/reference/{技术栈}-*.md`
5. `.agents/README.md`

## 验证

配置完成后，确认命令可用：
- `/piv:prime` - 输出项目概览
- `/piv:plan` - 创建计划
- `/piv:validate` - 运行验证
