---
description: 运行完整验证：lint + test + build
argument-hint: none
---

# /piv:validate：运行完整验证

## 验证层级

### 第一层：代码检查

```bash
[lint 命令]
```

### 第二层：单元测试

```bash
[test 命令]
```

### 第三层：覆盖率（如已配置）

```bash
[coverage 命令]
```

### 第四层：类型检查（如适用）

```bash
# TypeScript
npx tsc --noEmit

# Python
mypy app/
```

### 第五层：构建验证

```bash
# 前端
[package_manager] run build

# 后端（如适用）
[package_manager] run build
```

## 执行

按顺序运行所有层级。如果第一层失败，停止并修复，否则继续。

## 输出

```markdown
## 验证结果

### 第一层：代码检查
- 状态：通过 / 失败
- 输出：[...]

### 第二层：测试
- 状态：通过 / 失败
- 覆盖率：X%
- 失败的测试：[...]

### 第三层：构建
- 状态：通过 / 失败

## 总结
- 总检查数：N
- 通过：M
- 失败：K

## 需要采取的行动
- [ ] 修复 lint 问题
- [ ] 修复失败的测试
- [ ] 修复构建错误
```
