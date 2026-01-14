---
description: 同步配置：重新检测技术栈，更新相关文件
argument-hint: none
---

# /piv:sync：同步配置变更

## 适用场景

- 技术栈变更（如新增框架、切换数据库）
- 包管理器变更（如 npm → pnpm）
- 测试框架变更（如 pytest → vitest）
- 新增代码规范
- 项目目录结构重构

## 执行步骤

### 第一步：保存当前配置

```bash
# 记录当前扫描结果
cat > /tmp/piv-old-config.json <<EOF
{
  "scan_date": "$(date -Iseconds)",
  "files": $(git ls-files .claude/ .agents/ 2>/dev/null | wc -l)
}
EOF
```

### 第二步：重新扫描项目

运行 `/piv:scan` 获取新的检测结果。

### 第三步：比较配置差异

| 配置项 | 旧值 | 新值 | 需更新文件 |
|--------|------|------|------------|
| 语言 | Python | Python | 无需变更 |
| 框架 | FastAPI | FastAPI + Celery | commands、reference |
| 包管理器 | uv | pnpm | validate.md |
| ... | ... | ... | ... |

### 第四步：更新受影响文件

根据差异更新文件：

#### 4.1 技术栈相关命令更新

- `validation/validate.md` - 更新 lint、test、build 命令
- `core_piv_loop/*.md` - 更新验证命令
- `init-project.md` - 更新依赖安装命令

#### 4.2 参考文档更新

- 添加新的 best-practices.md
- 移除不再适用的参考文档
- 更新现有文档中的命令示例

#### 4.3 .agents/README.md 更新

- 更新技术栈说明
- 更新可用命令列表
- 更新验证命令

### 第五步：记录变更

创建 `.agents/CHANGELOG.md` 或在 README 中添加变更记录：

```markdown
## 配置变更记录

### [日期] by /piv:sync

#### 变更内容
- 技术栈：从 X 变更为 Y
- 包管理器：从 A 变更为 B
- 测试框架：从 C 变更为 D

#### 更新的文件
- `.claude/commands/validation/validate.md`
- `.claude/reference/new-framework.md`

#### 移除的文件
- `.claude/reference/old-framework.md`
```

## 输出

1. 更新后的 `.claude/commands/` 文件
2. 更新后的 `.claude/reference/` 文件
3. 更新后的 `.agents/README.md`
4. 变更记录

## 验证

同步完成后，运行以下命令验证：

```bash
/piv:validate    # 确认验证命令正确
/piv:prime       # 确认项目概览正确
```

## 回滚

如需回滚到之前的配置：

```bash
# 查看配置历史
git log --oneline --all -- .claude/ .agents/ | head -10

# 恢复到指定版本
git checkout <commit-hash> -- .claude/ .agents/
```
