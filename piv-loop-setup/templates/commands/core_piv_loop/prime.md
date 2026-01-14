---
description: 理解项目结构，输出项目概览
argument-hint: none
---

# /piv:prime：理解项目结构

## 执行步骤

### 第一步：列出项目文件

```bash
git ls-files
```

### 第二步：显示目录结构

```bash
# 显示项目主要目录
tree -L 2 -I 'node_modules|.git|__pycache__' .
```

### 第三步：阅读关键文档

按顺序阅读以下文件：

1. `CLAUDE.md` - 项目特定说明
2. `README.md` - 项目说明（如果存在）
3. 配置文件 - `package.json` / `pyproject.toml` / `pom.xml`
4. 编译配置 - `tsconfig.json` / `pyproject.toml`

### 第四步：识别关键文件

查找并阅读：

- 入口文件（main.py、index.ts、App.js）
- 配置文件
- 数据模型或模式定义
- API 路由/处理器

### 第五步：检查最近活动

```bash
git log --oneline -10
```

## 输出：项目概览报告

提供简洁的总结：

```markdown
## 项目概览

### 技术栈
- 语言：[语言]
- 框架：[框架]
- 包管理器：[包管理器]
- 测试框架：[测试框架]

### 关键文件
| 文件 | 用途 |
|------|------|
| `path/to/file.py` | 简要描述 |

### 代码规范
- 命名约定：[camelCase / snake_case / kebab-case]
- 风格：[观察到的关键模式]
- 错误处理：[使用的方法]

### 当前状态
- 最后提交：[哈希] - [消息]
- 待处理变更：[如果有]
- 已知问题：[如果有]
```

## 注意事项

- 专注于理解架构，不要急于实现
- 记录应该遵循的模式
- 识别潜在风险或复杂性
