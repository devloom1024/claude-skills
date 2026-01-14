# FastAPI 最佳实践

## 项目结构

```
app/
├── __init__.py
├── main.py           # 应用入口
├── router/           # API 路由
│   ├── __init__.py
│   ├── items.py
│   └── users.py
├── models/           # Pydantic 模型
├── services/         # 业务逻辑
├── repository/       # 数据访问
└── database.py       # 数据库连接
```

## API 设计

### 路由模式

```python
# app/router/items.py
from fastapi import APIRouter, HTTPException, status
from typing import List

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=List[Item])
async def list_items(skip: int = 0, limit: int = 100):
    return await repository.get_items(skip=skip, limit=limit)

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = await repository.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    return await repository.create_item(item)
```

### 错误处理

```python
# app/exception.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# 在 main.py 中
app.add_exception_handler(Exception, global_exception_handler)
```

## 依赖注入

```python
# app/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException
from app.services.auth import get_current_user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

## 验证

```python
from pydantic import BaseModel, Field, ConfigDict

class ItemCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    tax: float | None = Field(None, ge=0)
```

## 异步最佳实践

```python
# 全程使用 async
async def get_items() -> List[Item]:
    return await db.scalars(select(Item).offset(skip).limit(limit))

# 不要混用同步和异步
# 避免：asyncio.to_thread(blocking_io_call)
```
