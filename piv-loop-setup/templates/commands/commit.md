# /commit：创建提交

为所有未提交的更改创建新提交：

1. 运行 `git status && git diff HEAD && git status --porcelain`
2. 添加所有更改：`git add .`
3. 使用规范格式创建原子提交：

```
<类型>(<范围>): <主题>

<正文>

< footer>
```

类型：
- `feat`：新功能
- `fix`：修复 bug
- `docs`：文档更新
- `style`：格式调整
- `refactor`：重构
- `test`：测试
- `chore`：维护

示例：
```
feat(auth): 添加用户登录接口

- 实现基于 JWT 的身份验证
- 添加登录验证
- 包含刷新令牌机制

Closes #123
```
