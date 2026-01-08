# Obsidian to Anki 集成参考

本文件说明如何在学习项目中集成 Anki 卡片功能，使用 Obsidian to Anki 插件同步到 Anki。

**本文档基于 [Obsidian_to_Anki Wiki](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki) 编写。**

## ⚠️ 中文版 Anki 用户注意

如果你使用中文版 Anki，卡片格式会有所不同：

**问答题**：
- 使用 "问答题" 而非 "Basic"
- 使用 "正面:" 和 "背面:" 而非 "Front:" 和 "Back:"

**填空题**：
- 不需要标注 "Cloze" 或 "填空题"
- 直接写内容，使用 `{{c1::答案}}` 语法

**层级标签**：
- 使用 `::` 连接创建层级，如 `投资::永久投资组合::第1章::核心概念`

详见本文档末尾的"中文版 Anki 格式说明"部分。

---

## 目录结构

所有学习项目都应包含 `/anki-cards/` 目录，按日期组织：

```
/anki-cards/
  /YYYY-MM-DD/
    cards.md          # 该日生成的卡片
  anki-config.md      # Anki 配置说明
```

## Obsidian to Anki 基础语法

### 1. 指定卡片组（Deck）

在 md 文件顶部（任意位置，但建议顶部）：

```markdown
TARGET DECK: 学习项目名称
```

或者：

```markdown
TARGET DECK
学习项目名称
```

**重要**：
- 同一个学习项目的所有卡片应属于同一个 deck
- Deck 名称建议使用项目名称，例如：`《永久投资组合》学习`、`算法刷题`等

### 2. 文件级标签（可选）

为整个文件的所有卡片添加标签：

```markdown
FILE TAGS: 标签1 标签2 标签3
```

示例：
```markdown
FILE TAGS: 投资 第3章 风险管理
```

### 3. 基础正反卡片（Basic）

**完整格式**：
```markdown
START
Basic
Front: 什么是永久投资组合？
Back: 永久投资组合是由 Harry Browne 提出的投资策略，包含四种资产类别：25% 股票、25% 长期国债、25% 黄金、25% 现金。设计目标是在任何经济环境下都能保持稳定。
Tags: 投资策略 核心概念
END
```

**Inline 格式**（单行）：
```markdown
STARTI [Basic] Front: 什么是永久投资组合？ Back: 包含四种资产类别各25%：股票、长期国债、黄金、现金。 ENDI
```

### 4. 填空题（Cloze）

**标准 Anki 语法**：
```markdown
START
Cloze
Text: 永久投资组合包含 {{c1::四种}} 资产类别，每种占比 {{c2::25%}}。
Tags: 投资 数字
END
```

**简化语法**（需启用 CurlyCloze）：
```markdown
START
Cloze
Text: 永久投资组合包含 {四种} 资产类别，每种占比 {25%}。
Tags: 投资 数字
END
```

**带编号的填空**：
```markdown
START
Cloze
Text: 永久投资组合包含 {1:四种} 资产类别，每种占比 {2:25%}。
END
```

### 5. 问答卡片（多行回答）

```markdown
START
Basic
Front: 为什么永久投资组合选择这四种资产？
Back:
- **股票**：在经济繁荣期表现良好
- **长期国债**：在通缩或经济衰退期提供保护
- **黄金**：在通胀期保值
- **现金**：在利率上升期获益，提供流动性

这四种资产在不同经济周期中互补，确保投资组合的稳定性。
Tags: 投资原理 资产配置
END
```

## 生成卡片的最佳实践

### 1. 卡片粒度

**推荐做法**：
- ✅ 一个卡片对应一个小概念
- ✅ 问题清晰、具体
- ✅ 答案简洁，关键点突出
- ❌ 避免一个卡片包含太多信息

**示例对比**：

❌ **不好的卡片**（信息过多）：
```markdown
Front: 介绍永久投资组合
Back: 永久投资组合由 Harry Browne 在 1980 年代提出，包含股票、债券、黄金、现金四种资产，每种 25%，目的是应对不同经济环境，需要每年或资产偏离超过 15% 时再平衡...（太长）
```

✅ **好的卡片**（概念清晰）：
```markdown
Front: 永久投资组合的四种资产各占多少比例？
Back: 各占 25%（股票、长期国债、黄金、现金）
```

### 2. 卡片类型选择

**Basic（基础正反）**：
- 适合：定义、概念解释、原因说明
- 示例："什么是..."、"为什么..."、"如何..."

**Cloze（填空）**：
- 适合：数字、列表、关键术语、公式
- 示例：比例、步骤、分类

### 3. 标签策略

建议使用分层标签系统：

```markdown
FILE TAGS: {学科} {章节} {主题}
```

示例：
```markdown
FILE TAGS: 投资 第3章 资产配置
```

单卡片额外标签：
```markdown
Tags: 重点概念 公式 易错
```

## 自动生成卡片的时机

在学习会话中，以下情况应自动生成 Anki 卡片：

1. **学生掌握了新概念**
   - 理解检查通过
   - 可以用自己的话解释

2. **学习了重要的数字、公式、规则**
   - 需要记忆的事实性知识
   - 考试或实际应用中常用

3. **识别了关键的对比或区别**
   - A vs B 的区别
   - 不同方法的适用场景

4. **解决了练习题并理解原理**
   - 题目类型
   - 解题思路

## 卡片文件组织

### 文件命名

```
/anki-cards/YYYY-MM-DD/cards.md
```

### 文件结构模板（标准版）

```markdown
TARGET DECK: {学习项目名称}

FILE TAGS: {领域} {日期:YYYYMMDD}

# {会话主题} - Anki 卡片

本文件包含 YYYY-MM-DD 学习会话中生成的 Anki 卡片。

## 新学概念

START
Basic
Front: ...
Back: ...
Tags: 概念
END

## 重要数字/公式

START
Cloze
Text: ...
Tags: 数字 公式
END

## 对比/区别

START
Basic
Front: ...
Back: ...
Tags: 对比
END

---
**卡片统计**：本次会话生成 X 张卡片
```

## Claude 生成卡片的工作流

当 Claude 在学习会话中应该生成卡片时：

1. **识别可制卡知识点**
   - 在教学过程中注意学生掌握的知识点
   - 特别关注理解检查通过的内容

2. **创建/更新卡片文件**
   - 检查今天的 `/anki-cards/YYYY-MM-DD/cards.md` 是否存在
   - 不存在则创建，存在则追加

3. **生成合适的卡片**
   - 选择合适的卡片类型（Basic or Cloze）
   - 编写清晰的问题和简洁的答案
   - 添加合适的标签

4. **告知学生**
   - 在会话记录中提到："已为本次学到的概念生成 X 张 Anki 卡片"
   - 不需要详细展示卡片内容（已保存在文件中）

## 使用 Obsidian to Anki 同步

### 设置步骤（告知用户）：

1. **安装插件**
   - 在 Obsidian 中安装 "Obsidian_to_Anki" 插件
   - 确保 Anki 正在运行并安装了 AnkiConnect 插件

2. **配置插件**
   - 扫描目录：指向学习项目的 `/anki-cards/` 文件夹
   - 启用 "CurlyCloze" 选项（支持简化填空语法）

3. **同步卡片**
   - 在 Obsidian 中打开命令面板（Cmd/Ctrl + P）
   - 运行 "Obsidian_to_Anki: Scan directory"
   - 卡片会自动同步到 Anki 的指定 deck

4. **更新卡片**
   - 插件会自动识别已存在的卡片
   - 修改 md 文件后重新同步，保留学习进度

## 示例：完整的卡片文件（标准版）

```markdown
TARGET DECK: 《永久投资组合》学习

FILE TAGS: 投资 永久投资组合

# 永久投资组合基础概念 - Anki 卡片

本文件包含 2025-01-07 学习会话中生成的 Anki 卡片。

## 核心概念

START
Basic
Front: 什么是永久投资组合（Permanent Portfolio）？
Back: 由 Harry Browne 提出的投资策略，通过持有四种不同资产类别（各占25%）来应对任何经济环境：股票、长期国债、黄金、现金。
Tags: 核心定义
END

START
Cloze
Text: 永久投资组合包含 {{c1::四种}} 资产类别，分别是 {{c2::股票}}、{{c3::长期国债}}、{{c4::黄金}} 和 {{c5::现金}}，每种占比 {{c6::25%}}。
Tags: 组成 数字
END

## 投资原理

START
Basic
Front: 为什么永久投资组合选择股票作为资产之一？
Back: 股票在经济繁荣期（Prosperity）表现最好，可以对冲该时期的风险。
Tags: 资产原理 股票
END

START
Basic
Front: 永久投资组合中黄金的作用是什么？
Back: 黄金在通货膨胀（Inflation）期间保值，保护投资组合免受货币贬值影响。
Tags: 资产原理 黄金
END

## 再平衡规则

START
Cloze
Text: 永久投资组合建议在资产偏离目标配置超过 {{c1::15%}} 或 {{c2::每年}} 进行再平衡。
Tags: 操作 数字
END

---
**卡片统计**：本次会话生成 5 张卡片
```

## 领域特定的卡片策略

### 投资/理财
- 重点：概念定义、资产比例、投资原则
- 卡片类型：Basic（原理）+ Cloze（数字）

### 编程/算法
- 重点：算法思路、时间复杂度、代码模式
- 卡片类型：Basic（思路）+ Cloze（复杂度）+ 代码片段

### 职业认证
- 重点：考点、公式、规则、例外
- 卡片类型：Cloze（填空）为主，Basic（解释）为辅

### 语言学习
- 重点：词汇、语法规则、常用表达
- 卡片类型：Basic（翻译）+ Cloze（句子填空）

## 注意事项

1. **避免重复卡片**
   - 检查之前是否已为相同概念创建卡片
   - 可以在不同角度创建多张卡片，但避免完全重复

2. **保持一致性**
   - 同一项目的所有卡片使用相同的 deck 名称
   - 标签系统保持一致

3. **定期维护**
   - 每周或每月回顾卡片质量
   - 合并或删除低质量卡片
   - 更新过时信息

4. **与会话记录关联**
   - 在 session-notes.md 中提及生成了卡片
   - 方便日后回溯学习内容

---

## 中文版 Anki 格式说明

如果你使用**中文版 Anki**，卡片格式会有以下差异：

### 问答题格式

```markdown
START
问答题
正面: 问题内容
背面: 答案内容
Tags: 投资::永久投资组合::第X章::具体标签
<!--ID: 1766585436834-->
END
```

**关键差异**：
- 使用 `问答题` 而非 `Basic`
- 使用 `正面:` 和 `背面:` 而非 `Front:` 和 `Back:`
- `<!--ID: ...-->` 会在首次同步后自动生成，新卡片无需手动添加

### 填空题格式

```markdown
START
填空题内容，使用 {{c1::需要填空的答案}} 标记填空位置
Tags: 投资::永久投资组合::第X章::具体标签
END
```

**关键差异**：
- **不需要**标注 `Cloze` 或 `填空题`
- 直接写内容，使用标准的 `{{c1::答案}}` 语法

### 层级标签（重要）

中文版推荐使用 `::` 创建层级标签：

```markdown
Tags: 投资::永久投资组合::第1章::核心概念
```

**标签层级结构**：
```
领域::子领域::章节::具体分类
```

示例：
- `投资::永久投资组合::第1章::资产配置`
- `算法::动态规划::中等难度::背包问题`
- `语言::英语::语法::现在完成时`

### 文件 Frontmatter（YAML）

中文版卡片文件建议在开头添加 YAML frontmatter：

```markdown
---
创建时间: 2025-01-07
修改时间: 2025-01-07
会话主题: 永久投资组合基础概念
卡片数量: 5
---

TARGET DECK: 《永久投资组合》学习

FILE TAGS: 投资 永久投资组合

# 永久投资组合基础概念 - Anki 卡片
...
```

### 完整示例（中文版）

```markdown
---
创建时间: 2025-01-07
修改时间: 2025-01-07
会话主题: 永久投资组合核心概念
---

TARGET DECK: 《永久投资组合》学习

# 2025-01-07 学习卡片

## 核心定义

START
问答题
正面: 什么是永久投资组合？
背面: 由 Harry Browne 提出的投资策略，包含四种资产类别各占25%：股票、长期国债、黄金、现金。目标是应对任何经济环境。
Tags: 投资::永久投资组合::第1章::核心概念
END

## 数字记忆

START
永久投资组合包含 {{c1::四种}} 资产类别，每种占比 {{c2::25%}}。
Tags: 投资::永久投资组合::第1章::数字
END

START
永久投资组合建议在资产偏离目标配置超过 {{c1::15%}} 时进行再平衡。
Tags: 投资::永久投资组合::第2章::操作规则
END

---
**本次生成**: 3 张卡片
```

### Claude 生成中文版卡片时的注意事项

1. **自动识别版本**
   - 如果 CLAUDE.md 中指定使用中文版 Anki，自动使用中文格式
   - 默认使用标准英文格式

2. **层级标签自动生成**
   - 根据内容领域和章节自动生成层级标签
   - 格式：`{领域}::{子主题}::{章节}::{分类}`

3. **Frontmatter 自动添加**
   - 创建时间：当天日期
   - 修改时间：与创建时间相同（首次创建）
   - 会话主题：从 session-notes.md 获取

4. **ID 字段处理**
   - 新卡片不添加 ID
   - 让 Obsidian_to_Anki 插件在首次同步时自动生成

## 参考资源

- [Obsidian_to_Anki Wiki](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki)
- [Inline notes 语法](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Inline-notes)
- [Deck formatting](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Deck-formatting)
- [Tag formatting](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Tag-formatting)
- [Cloze formatting](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Cloze-formatting)
