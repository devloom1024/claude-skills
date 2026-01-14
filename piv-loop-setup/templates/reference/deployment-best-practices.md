# 部署最佳实践

## 环境配置

### 环境变量

```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key-here
LOG_LEVEL=INFO
```

### 密钥管理

- 永远不要将密钥提交到 git
- 使用环境变量或密钥管理工具
- 定期轮换密钥

## CI/CD 流水线

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 设置 {{language}}
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: 安装依赖
        run: {{install_command}}
      - name: 代码检查
        run: {{lint_command}}
      - name: 运行测试
        run: {{test_command}}
      - name: 构建
        run: {{package_manager}} run build
```

## 健康检查

### API 健康端点

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

@router.get("/ready")
def ready():
    # 检查依赖
    if db.is_connected() and redis.is_connected():
        return {"status": "ready"}
    return {"status": "not ready"}, 503
```

## 监控

### 关键指标

- 请求延迟（p50、p95、p99）
- 错误率
- 业务指标（转化率、注册量）
- 基础设施（CPU、内存、磁盘）

### 告警

| 严重程度 | 阈值 | 响应时间 |
|----------|------|----------|
| 严重 | 错误率 > 5% | < 15 分钟 |
| 警告 | 延迟 p95 > 1秒 | < 1 小时 |
| 信息 | 错误率 > 1% | < 24 小时 |

## 回滚策略

```bash
# Docker
docker rollback myapp

# Kubernetes
kubectl rollout undo deployment/myapp

# 数据库
psql -d db -f migrations/rollback_V2.sql
```
