---
name: piv-loop-setup
description: |
  为项目配置 PIV Loop AI 开发工作流。自动检测项目技术栈，生成 Claude Commands 命令模板，
  创建 .agents 目录结构和工作流文档。适用于新项目初始化、技术栈变更、规范更新等场景。

  使用场景：
  - 新项目需要设置 Claude Code 工作流（/piv:scan）
  - 项目处于设计阶段，无代码（/piv:design）
  - 技术栈或规范变更，需要同步更新（/piv:sync）
  - 团队需要统一的 AI 开发规范
---

# PIV Loop 工作流配置

## 快速开始

根据项目当前状态选择命令：

| 场景 | 命令 | 说明 |
|------|------|------|
| 设计阶段 | `/piv:design` | 根据需求生成项目结构和规范框架 |
| 已有代码 | `/piv:scan` | 检测技术栈，生成完整配置 |
| 配置更新 | `/piv:sync` | 重新检测，同步变更 |

## 工作流程

### 场景一：设计阶段（无代码）

```
需求 → /piv:design → .claude/PRD.md + 命令框架
```

**执行步骤：**

1. 阅读用户需求或 PRD 草稿
2. 生成 `.claude/PRD.md`（产品需求文档）
3. 创建 `.claude/commands/` 目录结构
4. 创建 `.agents/README.md`

### 场景二：扫描已有项目

```
代码 → /piv:scan → .claude/commands/ + .claude/reference/
```

**执行步骤：**

1. 扫描项目文件（package.json、pyproject.toml、pom.xml 等）
2. 检测技术栈（语言、框架、包管理器、测试框架）
3. 生成 `.claude/commands/` 下所有命令文件
4. 根据技术栈选择并生成 `.claude/reference/` 参考文档
5. 更新 `.agents/README.md`

### 场景三：同步配置

```
变更 → /piv:sync → 更新受影响文件
```

**执行步骤：**

1. 重新扫描项目，检测变更
2. 比较新旧配置差异
3. 只更新受影响的部分
4. 记录变更日志

## PIV Loop 核心流程

无论哪个场景，都遵循 PIV Loop：

```
PRIME（理解）→ PLAN（规划）→ EXECUTE（执行）→ VALIDATE（验证）
     ↓              ↓              ↓              ↓
   了解项目      创建计划       编码实现       测试/lint
```

### 命令说明

| 命令 | 描述 | 适用阶段 |
|------|------|----------|
| `/piv:prime` | 理解项目结构，输出概览 | 任何阶段 |
| `/piv:plan` | 创建详细实施计划 | PLAN |
| `/piv:execute` | 按计划执行实现 | EXECUTE |
| `/piv:validate` | 运行 lint + test + build | VALIDATE |

## 输出文件结构

```
.claude/
├── commands/           # 命令模板
│   ├── core_piv_loop/  # PIV 循环命令
│   │   ├── prime.md
│   │   ├── plan.md
│   │   └── execute.md
│   ├── validation/     # 验证命令
│   │   └── validate.md
│   └── commit.md
├── reference/          # 参考文档
│   └── {技术栈}-best-practices.md
└── PRD.md              # 产品需求文档（设计阶段）
.agents/
├── plans/              # 实施计划
├── code-reviews/       # 代码审查
└── README.md           # 工作流说明
```

## 验证配置

配置完成后，确认以下命令可用：

```bash
/piv:prime     # 应输出项目概览
/piv:plan      # 应能创建计划
/piv:validate  # 应运行 lint + test
```

## 故障排除

### 命令未显示

- 重新加载 Claude Code 窗口（Cmd+Shift+P：Reload Window）
- 检查 `.claude/commands/` 目录存在且包含 .md 文件

### 扫描结果不准确

- 创建 `piv-config.json` 手动指定配置
- 运行 `/piv:scan --debug` 查看检测日志
