# /init-project：初始化项目

在本地设置并启动 {{project_name}} 应用程序。

## 第一步：安装依赖

```bash
[install 命令]
```

## 第二步：启动开发服务器

```bash
[run 命令] dev
```

## 第三步：验证设置

```bash
# 检查服务器运行状态
curl -s http://localhost:3000

# 运行健康检查（如有）
[run 命令] test
```

## 访问地址
- **前端**：http://localhost:3000
- **API**：http://localhost:8000（如适用）
- **文档**：http://localhost:8000/docs（如适用）

## 注意事项
- 查看 `package.json` / `pyproject.toml` 了解可用的脚本
- 数据库可能需要迁移：`[run 命令] db:migrate`
