# SQLite 最佳实践

## 连接管理

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine(
    "sqlite:///./habits.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 模式设计

```python
# models/habit.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # 关系
    completions = relationship("HabitCompletion", back_populates="habit")

class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    note = Column(String(200))

    habit = relationship("Habit", back_populates="completions")
```

## 迁移（Alembic）

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from app.models import Base
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()
```

## 查询模式

```python
# repositories/habit_repo.py
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import Habit, HabitCompletion

class HabitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, habit_id: int) -> Habit | None:
        return self.db.scalar(select(Habit).where(Habit.id == habit_id))

    def get_all_active(self) -> list[Habit]:
        return list(
            self.db.scalars(
                select(Habit)
                .where(Habit.is_active == True)
                .order_by(Habit.created_at.desc())
            )
        )

    def get_streak(self, habit_id: int) -> int:
        """计算当前连续天数"""
        from sqlalchemy import desc
        completions = (
            self.db.scalars(
                select(HabitCompletion)
                .where(HabitCompletion.habit_id == habit_id)
                .order_by(desc(HabitCompletion.completed_at))
            )
            .all()
        )
        # 连续天数计算逻辑
        return streak

    def create(self, habit: Habit) -> Habit:
        self.db.add(habit)
        self.db.commit()
        self.db.refresh(habit)
        return habit

    def delete(self, habit_id: int) -> bool:
        habit = self.get_by_id(habit_id)
        if habit:
            self.db.delete(habit)
            self.db.commit()
            return True
        return False
```

## 性能索引

```python
class Habit(Base):
    # ...

# 为频繁查询的列添加索引
__table_args__ = (
    Index('idx_habit_name', 'name'),
    Index('idx_completion_habit_date', 'habit_id', 'completed_at'),
)
```
