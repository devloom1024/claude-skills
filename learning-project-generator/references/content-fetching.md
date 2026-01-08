# 内容获取与保存指南

当用户提供 URL 时，采用**按需获取**策略：初始化时只获取目录页，学习时按需获取具体章节并缓存，实现一次获取、重复使用。

## 核心策略：按需获取 + 本地缓存

### 优势

1. **快速初始化**：项目生成时不需要等待大量内容抓取
2. **节省资源**：只获取用户实际需要的内容
3. **避免重复**：每个页面只获取一次，后续直接使用缓存
4. **灵活扩展**：用户可以随时获取新的章节内容

### 三阶段工作流程

```
项目初始化 → 按需获取 → 本地缓存
   (快)         (按需)      (重复使用)
```

## 阶段 1：项目初始化（生成项目时）

### 1.1 检测 firecrawl MCP 可用性

优先使用 firecrawl MCP（如果可用），因为它提供更可靠的内容抓取和更好的格式化。

**检测方法**：检查是否有 `mcp__firecrawl-mcp__firecrawl_scrape` 工具。

### 1.2 只获取主页面/目录页内容

**目标**：快速获取课程大纲/目录结构，不获取所有章节内容。

#### 使用 firecrawl（首选）

```javascript
mcp__firecrawl-mcp__firecrawl_scrape({
  url: "用户提供的URL",
  formats: ["markdown"],
  onlyMainContent: true
})
```

**优势**：
- 自动转换为 markdown 格式
- 提取主要内容，过滤广告和导航
- 更可靠的内容抓取

#### 使用 WebFetch（降级方案）

```javascript
WebFetch({
  url: "用户提供的URL",
  prompt: "请提取这个页面的完整目录结构、章节标题和链接。保持原有的结构层次。"
})
```

### 1.3 分析并记录可用链接

分析获取的目录页内容，识别：
- **章节链接**：第1章、第2章等
- **模块链接**：基础篇、进阶篇等
- **资源链接**：练习题、参考资料等

**重要**：只记录链接，不立即获取内容。

### 1.4 创建链接索引

在 `/materials/` 目录下创建文件：

#### 保存目录页内容：`main.md`

```markdown
---
source_url: https://example.com/course
fetch_date: 2026-01-08
title: 课程主页
status: fetched
---

# 课程主页

[目录页的完整内容...]

## 课程目录

- 第1章：简介
- 第2章：基础概念
- ...

---

**来源**：[原始页面](https://example.com/course)
**抓取时间**：2026-01-08
```

#### 创建链接索引：`README.md`

```markdown
# 学习材料

本目录使用**按需获取**策略管理学习材料。

## 📋 材料索引

### 主页 / 目录

- ✅ [main.md](main.md) - 课程主页/概览
  - 来源：https://example.com/course
  - 状态：已获取

### 章节内容

以下章节将在学习时按需获取：

- ⏳ **第1章：数组基础** - `chapter-01.md`
  - 来源：https://example.com/chapter-01
  - 状态：未获取（首次使用时会自动获取）

- ⏳ **第2章：排序算法** - `chapter-02.md`
  - 来源：https://example.com/chapter-02
  - 状态：未获取

- ⏳ **第3章：搜索算法** - `chapter-03.md`
  - 来源：https://example.com/chapter-03
  - 状态：未获取

[... 更多章节]

## 📊 获取状态

- ✅ 已获取：1 个（主页）
- ⏳ 待获取：15 个（将在学习时按需获取）

## 🔄 按需获取说明

**这些材料采用按需获取策略**：
- **初始化时**：只获取主页/目录页
- **学习时**：当你询问某个章节时，Claude 会自动：
  1. 检查本地是否已有该文件
  2. 如果没有，使用 firecrawl 获取并保存
  3. 如果有，直接读取使用
  4. 更新此索引文件的状态

**优势**：
- 快速初始化，不需要等待
- 只获取你实际需要的内容
- 每个页面只获取一次，后续直接使用
- 节省时间和资源

## 📝 使用说明

在学习过程中：
1. 直接向 Claude 提问（如："讲解第3章的内容"）
2. Claude 会自动检查并获取材料
3. 获取后的内容会保存到本地
4. 下次使用时直接读取，无需再次获取

## 🔗 原始链接

如果需要访问原始网页：[https://example.com/course](https://example.com/course)
```

#### 创建链接映射：`links-map.json`（机器可读）

```json
{
  "base_url": "https://example.com",
  "fetched_pages": [
    {
      "title": "课程主页",
      "url": "https://example.com/course",
      "filename": "main.md",
      "status": "fetched",
      "fetch_date": "2026-01-08"
    }
  ],
  "pending_pages": [
    {
      "title": "第1章：数组基础",
      "url": "https://example.com/chapter-01",
      "filename": "chapter-01.md",
      "status": "pending"
    },
    {
      "title": "第2章：排序算法",
      "url": "https://example.com/chapter-02",
      "filename": "chapter-02.md",
      "status": "pending"
    }
  ]
}
```

**用途**：Claude 在学习阶段可以读取此文件，快速找到需要获取的 URL。

## 阶段 2：按需获取（学习时）

### 2.1 触发时机

当用户询问某个章节/主题时，Claude 应该：
1. 识别用户想要学习的内容（如："讲解第3章"）
2. 检查 `/materials/` 目录是否已有对应文件
3. 如果没有，触发获取流程

### 2.2 检查本地缓存

**步骤 1**：读取 `links-map.json` 找到对应的 URL 和文件名

```javascript
// 伪代码
const map = Read('/materials/links-map.json')
const chapter = map.pending_pages.find(p => p.title.includes('第3章'))
// 结果：{ filename: 'chapter-03.md', url: 'https://...' }
```

**步骤 2**：检查文件是否已存在

```bash
# 使用 Bash 工具检查
ls /path/to/project/materials/chapter-03.md
```

**步骤 3**：根据结果决定操作
- **文件存在** → 直接读取并使用
- **文件不存在** → 执行获取流程（见 2.3）

### 2.3 执行获取流程

#### 使用 firecrawl 获取内容（首选）

```javascript
mcp__firecrawl-mcp__firecrawl_scrape({
  url: chapter.url,  // 从 links-map.json 读取
  formats: ["markdown"],
  onlyMainContent: true
})
```

#### 保存到本地

使用 Write 工具保存内容：

```markdown
---
source_url: https://example.com/chapter-03
fetch_date: 2026-01-08
title: 第3章：搜索算法
status: fetched
---

# 第3章：搜索算法

[章节的完整内容...]

---

**来源**：[原始页面](https://example.com/chapter-03)
**抓取时间**：2026-01-08
```

#### 更新索引文件

1. **更新 README.md**：将该章节从 ⏳ 改为 ✅
2. **更新 links-map.json**：将该页面从 `pending_pages` 移到 `fetched_pages`

```json
{
  "fetched_pages": [
    {
      "title": "第3章：搜索算法",
      "url": "https://example.com/chapter-03",
      "filename": "chapter-03.md",
      "status": "fetched",
      "fetch_date": "2026-01-08"
    }
  ]
}
```

### 2.4 处理获取失败

如果获取失败：

1. **记录失败信息**：追加到 `failed-links.md`

```markdown
# 无法获取的链接

## 失败列表

### 第3章：搜索算法
- **URL**：https://example.com/chapter-03
- **失败原因**：请求超时
- **尝试时间**：2026-01-08
- **建议**：稍后重试，或手动访问该页面复制内容保存为 `chapter-03.md`
```

2. **告知用户**：明确说明无法获取，提供原始链接

```
抱歉，我无法自动获取第3章的内容（请求超时）。
你可以：
1. 稍后让我重试
2. 手动访问：https://example.com/chapter-03
3. 暂时跳过这一章
```

3. **不要编造内容**：绝不基于猜测或训练数据回答章节内容

## 阶段 3：本地缓存（重复使用）

### 3.1 直接使用已获取的内容

当用户再次询问已获取的章节时：

1. 检查 `links-map.json` → 状态为 `fetched`
2. 直接读取本地文件
3. 基于文件内容回答

**无需再次获取**，实现真正的"一次获取，重复使用"。

### 3.2 更新过期内容（可选）

如果用户认为内容过期，可以重新获取：

```
用户："第3章的内容好像更新了，能重新获取吗？"
Claude：
1. 使用 firecrawl 重新获取
2. 覆盖 chapter-03.md
3. 更新 fetch_date 字段
```

## 在生成的 CLAUDE.md 中添加指令

在生成的项目 `CLAUDE.md` 文件中，添加按需获取材料的指令：

```markdown
### 学习材料引用规则

本项目使用**按需获取**策略管理学习材料，位于 `/materials/` 目录。

**重要**：在回答用户问题时，你**必须**：

#### 1. 检查本地材料

在回答前，检查是否已有相关材料：

**步骤**：
1. 读取 `/materials/links-map.json` 了解材料索引
2. 检查用户询问的章节/主题是否已获取（`status: "fetched"`）
3. 如果已获取，使用 Read 工具读取对应的 md 文件
4. 如果未获取，执行获取流程（见下文）

#### 2. 按需获取缺失的材料

如果用户询问的内容尚未获取：

**步骤**：
1. 从 `links-map.json` 找到对应的 URL 和文件名
2. 使用 firecrawl（首选）或 WebFetch 获取内容
3. 保存为 markdown 文件到 `/materials/` 目录
4. 更新 `links-map.json` 的状态为 `fetched`
5. 更新 `/materials/README.md` 的获取状态（⏳ → ✅）
6. 基于获取的内容回答用户问题

**示例**：

```
用户："讲解第3章的内容"

你的操作：
1. 读取 links-map.json → 找到 chapter-03.md (pending)
2. 检查文件是否存在 → 不存在
3. 从 map 获取 URL: https://example.com/chapter-03
4. 使用 firecrawl_scrape 获取内容
5. 保存到 materials/chapter-03.md
6. 更新 links-map.json 和 README.md
7. 读取 chapter-03.md 并回答用户
```

#### 3. 明确引用来源

在回答时：
- 注明引用的文件：`根据 [chapter-03.md](materials/chapter-03.md)，第3章主要讲解了...`
- 如果材料中没有答案，明确告知用户
- 提供原始链接供用户参考

#### 4. 不要凭空猜测

**严格禁止**：
- ❌ 在材料未获取时，基于你的训练数据猜测章节内容
- ❌ 假装已经获取了材料，但实际上是编造的
- ❌ 不告知用户就使用非本地材料的信息

**正确做法**：
- ✅ 明确告知正在获取材料："让我先获取第3章的内容..."
- ✅ 获取后再回答，或告知获取失败
- ✅ 如果获取失败，提供原始链接，建议用户手动查看

#### 5. 处理获取失败

如果获取失败：
1. 记录到 `/materials/failed-links.md`
2. 明确告知用户失败原因
3. 提供原始链接
4. 不要基于猜测回答内容

#### 示例工作流程

##### 场景 1：首次询问某章节

```
用户："第3章讲了什么？"

Claude 的操作：
1. 读取 links-map.json → chapter-03.md (pending)
2. "让我先获取第3章的内容..."
3. 使用 firecrawl 获取
4. 保存到 materials/chapter-03.md
5. 更新索引文件
6. "根据 [chapter-03.md](materials/chapter-03.md)，第3章主要讲解了..."
```

##### 场景 2：再次询问已获取的章节

```
用户："再给我复习一下第3章"

Claude 的操作：
1. 读取 links-map.json → chapter-03.md (fetched)
2. 直接读取 materials/chapter-03.md
3. "根据 [chapter-03.md](materials/chapter-03.md)，让我帮你复习..."
```

##### 场景 3：获取失败

```
用户："讲解第5章"

Claude 的操作：
1. 尝试获取 → 失败（超时）
2. 记录到 failed-links.md
3. "抱歉，无法自动获取第5章的内容（请求超时）。你可以访问原始链接：https://example.com/chapter-05"
```
```

## 实施清单

在实施按需获取策略时，确保完成：

### 项目初始化阶段
- [ ] 检测 firecrawl MCP 可用性
- [ ] 只获取主页面/目录页内容
- [ ] 分析内容结构，识别所有章节/模块链接
- [ ] 保存主页内容为 `materials/main.md`
- [ ] 创建 `materials/README.md` 索引（标记待获取的章节）
- [ ] 创建 `materials/links-map.json` 链接映射
- [ ] 在生成的 `CLAUDE.md` 中添加按需获取指令
- [ ] 告知用户采用按需获取策略，无需等待

### 学习阶段（由 Claude 执行）
- [ ] 识别用户询问的章节/主题
- [ ] 读取 `links-map.json` 查找对应链接
- [ ] 检查本地文件是否已存在
- [ ] 如果不存在，使用 firecrawl 获取内容
- [ ] 保存为 markdown 文件
- [ ] 更新 `links-map.json` 状态
- [ ] 更新 `README.md` 获取状态
- [ ] 如果获取失败，记录到 `failed-links.md`
- [ ] 基于获取的内容回答用户问题

## 常见场景

### 场景 1：单页教程

**例子**：https://example.com/tutorial

**操作**：
1. 获取该页面内容
2. 保存为 `materials/main.md`
3. 创建简单的 `materials/README.md`
4. `links-map.json` 只包含一个页面

**无需按需获取**，因为只有一个页面。

### 场景 2：多章节课程

**例子**：https://example.com/course（包含 15 个章节链接）

**初始化操作**：
1. 获取主页内容，保存为 `materials/main.md`
2. 从主页提取所有章节链接（15个）
3. 创建 `materials/README.md`，列出15个待获取的章节
4. 创建 `links-map.json`，记录15个章节的 URL 和文件名
5. **不立即获取这15个章节**

**学习时操作**：
- 用户问第3章 → 获取并保存 `chapter-03.md`
- 用户问第7章 → 获取并保存 `chapter-07.md`
- 用户从不问第10章 → 永远不获取第10章（节省资源）

### 场景 3：用户跳过某些章节

**例子**：用户只学习第1、3、5章

**结果**：
- 获取的文件：`main.md`、`chapter-01.md`、`chapter-03.md`、`chapter-05.md`
- 未获取的文件：第2、4、6-15章
- 节省了大量时间和资源

### 场景 4：获取失败的处理

**例子**：第5章的链接失效

**操作**：
1. 用户问第5章时，尝试获取
2. 获取失败（404）
3. 记录到 `materials/failed-links.md`
4. 告知用户："无法获取第5章（页面不存在）。原始链接：..."
5. 继续正常获取其他章节

## 性能优化

### 避免重复获取

- 每次获取前检查 `links-map.json` 的状态
- 状态为 `fetched` → 直接使用本地文件
- 状态为 `pending` → 执行获取流程

### 批量获取（可选）

如果用户一次询问多个章节（如："讲解第3、4、5章"）：

```javascript
// 并行获取多个章节
Promise.all([
  firecrawl_scrape({ url: chapter3Url, ... }),
  firecrawl_scrape({ url: chapter4Url, ... }),
  firecrawl_scrape({ url: chapter5Url, ... })
])
```

### 超时处理

- 单个页面获取超时（>30秒） → 记录到 failed-links.md
- 不阻塞用户继续学习其他内容

## 与传统方法对比

| 特性 | 传统方法（全量获取） | 按需获取 + 缓存 |
|------|----------------------|-----------------|
| 初始化时间 | 慢（需获取所有内容） | 快（只获取目录页） |
| 资源使用 | 高（获取所有页面） | 低（只获取需要的） |
| 灵活性 | 低（一次性获取） | 高（随时获取新内容） |
| 用户体验 | 需要等待 | 立即开始学习 |
| 重复获取 | 否 | 否（使用本地缓存） |
| 适用场景 | 内容少、链接稳定 | 内容多、按需学习 |

## 总结

按需获取策略的核心：
1. **初始化时**：只获取目录，记录所有链接
2. **学习时**：按需获取具体章节并保存
3. **后续使用**：直接读取本地缓存

**结果**：快速初始化 + 节省资源 + 避免重复 + 灵活扩展
