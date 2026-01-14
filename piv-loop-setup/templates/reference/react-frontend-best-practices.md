# React 前端最佳实践

## 项目结构

```
src/
├── components/       # 可复用 UI 组件
│   ├── ui/          # 基础组件（Button、Input）
│   ├── layout/      # 布局组件
│   └── features/    # 功能特定组件
├── hooks/            # 自定义 React Hooks
├── services/         # API 客户端
├── stores/           # 状态管理
├── utils/            # 辅助函数
├── types/            # TypeScript 类型
└── pages/            # 路由页面
```

## 组件模式

### 使用 Hooks 的函数组件

```tsx
// components/UserProfile.tsx
import { useQuery } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';

interface UserProfileProps {
  userId: string;
}

export function UserProfile({ userId }: UserProfileProps) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 分钟
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage />;

  return (
    <div className="user-profile">
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### 自定义 Hook

```tsx
// hooks/useForm.ts
import { useState, useCallback } from 'react';

interface FormState<T> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
}

export function useForm<T extends Record<string, unknown>>(
  initialValues: T,
  validate: (values: T) => Partial<Record<keyof T, string>>
) {
  const [state, setState] = useState<FormState<T>>({
    values: initialValues,
    errors: {},
    touched: {},
  });

  const handleChange = useCallback((name: keyof T, value: unknown) => {
    setState(prev => ({
      ...prev,
      values: { ...prev.values, [name]: value },
    }));
  }, []);

  const handleBlur = useCallback((name: keyof T) => {
    setState(prev => ({
      ...prev,
      touched: { ...prev.touched, [name]: true },
      errors: { ...prev.errors, ...validate(prev.values) },
    }));
  }, [validate]);

  return { state, handleChange, handleBlur };
}
```

## 状态管理

### React Query（服务端状态）

```tsx
// services/api.ts
import { queryClient } from './queryClient';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// 使用失效的 Mutations
const mutation = useMutation({
  mutationFn: createItem,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['items'] });
  },
});
```

### Zustand（客户端状态）

```tsx
// stores/cartStore.ts
import { create } from 'zustand';

interface CartItem {
  id: string;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clear: () => void;
}

export const useCartStore = create<CartStore>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({
    items: [...state.items, item],
  })),
  removeItem: (id) => set((state) => ({
    items: state.items.filter((i) => i.id !== id),
  })),
  clear: () => set({ items: [] }),
}));
```

## 性能优化

```tsx
// Memoize 昂贵的计算
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);

// Memoize 回调
const handleClick = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// Memoize 组件
const ExpensiveComponent = memo(function ExpensiveComponent({
  data
}: Props) {
  // ...
});
```
