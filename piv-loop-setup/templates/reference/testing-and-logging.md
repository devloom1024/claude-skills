# 测试与日志最佳实践

## 测试策略

### 测试金字塔

```
        /\
       /  \      E2E 测试（少量）
      /____\
     /      \     集成测试（一些）
    /________\
   /          \    单元测试（大量）
  /____________\
```

### 单元测试

```python
# test_feature.py
import pytest
from app.feature import calculate

def test_calculate_basic():
    assert calculate(2, 3) == 5

def test_calculate_edge_cases():
    assert calculate(0, 0) == 0
    assert calculate(-1, 1) == 0

def test_calculate_invalid_input():
    with pytest.raises(ValueError):
        calculate("invalid", 1)
```

### 集成测试

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## 日志规范

### 结构化日志

```python
import structlog

logger = structlog.get_logger()

def process_user(user_id: int):
    logger.info(
        "user.processing",
        user_id=user_id,
        action="start"
    )
    try:
        result = do_processing(user_id)
        logger.info(
            "user.processed",
            user_id=user_id,
            result="success"
        )
        return result
    except Exception as e:
        logger.error(
            "user.processing_failed",
            user_id=user_id,
            error=str(e)
        )
        raise
```

### 日志级别

| 级别 | 使用场景 |
|------|----------|
| DEBUG | 调试详细信息 |
| INFO | 正常操作 |
| WARNING | 意外但非错误 |
| ERROR | 操作失败 |
| CRITICAL | 系统不可用 |

### 日志关键字段

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "event": "user.login",
  "user_id": 123,
  "session_id": "abc123",
  "duration_ms": 45
}
```
