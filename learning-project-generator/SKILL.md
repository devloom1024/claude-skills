---
name: learning-project-generator
description: 为书籍或在线课程内容生成定制化的 AI 辅助学习项目结构。使用苏格拉底教学法创建个性化的学习环境，包含会话追踪、进度监控和知识盲区识别。当用户想要为书籍（如《哈利布朗永久投资组合》）或在线教程/课程（如 labuladong 算法教程）创建结构化学习项目时使用。支持多种学习领域：投资理财、编程算法、职业认证、语言学习、学术科目、技能手艺等。
---

# 学习项目生成器

这个 skill 为任何学习内容（书籍或在线资源）生成定制化的 AI 辅助学习项目结构。

## 核心理念

**不死板的模板**：根据内容类型、学习目标和领域特点智能调整项目结构，而非生成固定的目录结构。

**关键原则**：
- 深入分析内容，理解学习目标
- 识别学习领域（投资、编程、认证考试等）
- 应用领域特定的定制化模式
- 添加内容独有的目录和追踪维度
- 保持核心学习方法一致（苏格拉底教学法 + 会话追踪）

## 使用流程

### 1. 收集输入信息

询问用户三个关键信息：

```
为了生成最适合你的学习项目，我需要了解：

1. **学习内容**：
   - 书籍名称（如：《哈利布朗永久投资组合》）
   - 或者 URL 地址（如：https://labuladong.online/zh/algo/intro/quick-learning-plan）

2. **输出路径**：
   项目应该创建在哪个目录？（提供绝对路径）

3. **学习目标**（可选）：
   - 你的学习目标是什么？（例如：通过考试、掌握技能、应用到工作中）
   - 有时间限制吗？（例如：3个月后考试）
```

### 2. 分析内容

**如果是 URL**：
- **优先使用 firecrawl MCP**（如果可用）：检查是否有 `mcp__mcp-server-firecrawl__firecrawl_scrape` 工具
  - 使用 firecrawl 获取内容更可靠、格式更好
  - 详见 `references/content-fetching.md` 了解完整的内容获取和保存流程
- **降级方案**：如果 firecrawl 不可用，使用 WebFetch 获取内容
- 分析页面结构、章节目录、学习路径
- 识别内容类型（教程、课程、文档等）
- **保存内容到项目**：将获取的内容转换为 markdown 并保存到 `/materials/` 目录（详见下文）

**如果是书籍**：
- 基于书名和你的知识判断内容主题
- 如果不熟悉，使用 WebSearch 搜索书籍信息
- 了解章节结构、主要概念、目标读者

**分析维度**：
1. **主题领域**：投资、编程、考试、语言等
2. **内容结构**：章节式、主题式、项目式
3. **学习深度**：入门、中级、高级
4. **实践性质**：理论为主、实践为主、理论+实践

### 3. 选择定制化模式

参考 `references/domain-templates.md` 中的领域模板，选择最适合的模式。

**选择逻辑**：
1. 识别主要学习领域
2. 确定是否需要混合多个领域的特点
3. 基于内容结构调整追踪维度
4. 添加内容特定的目录和文件

**重要**：不要机械套用模板！要根据具体内容灵活调整。

### 4. 生成项目结构

使用 `assets/core-template/` 中的模板文件，填充变量并生成定制化内容。

**生成步骤**：

#### 4.1 创建基础目录结构

```bash
mkdir -p {output_path}/{project-name}/sessions
mkdir -p {output_path}/{project-name}/progress
mkdir -p {output_path}/{project-name}/anki-cards
mkdir -p {output_path}/{project-name}/materials
```

**重要**：
- 所有项目都应包含 `/anki-cards/` 目录用于存储 Anki 卡片
- 所有项目都应包含 `/materials/` 目录用于存储学习材料（如果提供了 URL）

#### 4.2 根据领域添加额外目录

示例：
- 编程类：添加 `/solutions/`、`/patterns/`
- 投资类：添加 `/portfolio/`、`/market-research/`
- 考试类：添加 `/practice-tests/`、`/formulas/`

**注意**：`/anki-cards/` 是所有项目的标准配置，不属于额外目录。

#### 4.2.1 为空目录添加 .gitkeep

**重要**：为所有空目录创建 `.gitkeep` 文件，防止提交到 git 时目录丢失。

使用 Write 工具在每个空目录中创建 `.gitkeep` 文件：

```
{output_path}/{project-name}/sessions/.gitkeep
{output_path}/{project-name}/progress/.gitkeep
{output_path}/{project-name}/anki-cards/.gitkeep
{output_path}/{project-name}/materials/.gitkeep (如果该目录初始为空)
{output_path}/{project-name}/{额外目录}/.gitkeep
```

`.gitkeep` 文件内容可以是空的，或者添加简单说明：
```
# This file ensures the directory is tracked by git
```

**注意**：如果目录中已经有文件（如 materials 目录中保存了学习内容），则不需要添加 `.gitkeep`。

#### 4.3 生成 README.md

从 `assets/core-template/README.md.template` 开始，替换变量：

**基础变量**：
- `{{PROJECT_NAME}}` - 项目名称
- `{{SUBJECT_NAME}}` - 学习主题
- `{{CONTENT_DESCRIPTION}}` - 内容描述
- `{{CREATION_DATE}}` - 创建日期

**定制化变量**：
- `{{CUSTOM_OVERVIEW}}` - 领域特定的概述（如：考试日期、投资目标等）
- `{{DIRECTORY_TREE}}` - 实际生成的目录树
- `{{STRUCTURE_EXPLANATION}}` - 解释为什么选择这个结构
- `{{STUDY_MATERIALS}}` - 学习材料说明
- `{{CUSTOM_USAGE}}` - 领域特定的使用说明
- `{{FREE_RESOURCES}}` - 免费资源（如果适用）
- `{{CUSTOM_FOOTER}}` - 额外信息

#### 4.4 生成 CLAUDE.md

从 `assets/core-template/CLAUDE.md.template` 开始，填充：

**核心变量**：
- `{{PROJECT_NAME}}` - 项目名称
- `{{SUBJECT_DESCRIPTION}}` - 主题描述
- `{{TUTOR_ROLE_TITLE}}` - 导师角色标题
- `{{SUBJECT_NAME}}` - 学科名称
- `{{CONTEXT_EXAMPLES}}` - 领域特定示例
- `{{EXAMPLE_QUESTION}}` - 示例学生问题
- `{{PROBE_EXISTING_KNOWLEDGE}}` - 探测现有知识的问题
- `{{EXAMPLE_EXPLANATION}}` - 示例解释
- `{{COMPREHENSION_CHECK_QUESTION}}` - 理解检查问题

**领域特定内容**：
- `{{DOMAIN_SPECIFIC_CONTEXT}}` - 完整的领域背景（如：CFP 考试的知识领域、算法分类等）
- `{{AUTHORITATIVE_SOURCES}}` - 权威来源列表
- `{{ALWAYS_SEARCH_EXAMPLES}}` - 总是需要搜索的内容类型
- `{{PRIMARY_GOAL}}` - 主要学习目标
- `{{STAKES}}` - 学习的重要性（如：职业、考试、技能）
- `{{ORGANIZATION_SCHEME}}` - 组织方案（如：按考试领域、按章节、按难度）
- `{{PRIORITY_FACTORS}}` - 优先级因素（如：考试权重、项目截止日期）
- `{{ROADMAP_TYPE}}` - 路线图类型（如：考试路线图、技能路线图）
- `{{MATERIALS_USAGE_INSTRUCTIONS}}` - 学习材料引用说明（如果提供了 URL 并获取了内容）

**关于 MATERIALS_USAGE_INSTRUCTIONS**：

如果用户提供了 URL 且成功获取了内容到 `/materials/` 目录，填充此变量为：

```markdown
**重要**：本项目包含预先获取的学习材料，位于 `/materials/` 目录。

在回答用户问题时，你**必须**：

1. **优先引用本地材料**
   - 在回答前，先检查 `/materials/README.md` 了解可用的材料
   - 根据用户问题，使用 Read 工具读取相关的 markdown 文件
   - 基于材料内容回答，而不是依赖你的训练数据

2. **明确引用来源**
   - 在回答时注明引用的文件：`根据 [chapter-01.md](materials/chapter-01.md) 的内容...`
   - 如果材料中没有答案，明确告知用户："我在学习材料中没有找到关于X的信息"

3. **不要凭空猜测**
   - 如果材料中没有相关信息，**不要自己编造**
   - 告诉用户："学习材料中没有涉及这个话题，建议查看原始链接或其他资源。"
   - 如果有 `failed-links.md`，可以提示用户查看缺失的内容

4. **材料更新提醒**
   - 如果发现材料过时或有误，提醒用户更新材料
   - 如果用户补充了内容，记录到会话笔记中

**示例工作流程**：

学生问："第3章讲了什么？"

正确做法：
1. 读取 `/materials/chapter-03.md`
2. 总结章节内容
3. 回答："根据 [chapter-03.md](materials/chapter-03.md)，第3章主要讲解了..."

错误做法（禁止）：
- ❌ 不读取材料，直接基于你的知识回答
- ❌ 假装读了材料，但实际上是编造的
```

如果**没有**提供 URL 或未获取材料，填充此变量为：

```markdown
本项目没有预先获取的学习材料。在回答用户问题时，基于你的知识和用户提供的信息进行教学。
```

#### 4.5 生成 study-tracker.md

从 `assets/core-template/progress/study-tracker.md.template` 开始：

**需要定制的部分**：
- `{{SUBJECT_NAME}}` - 学科名称
- `{{CUSTOM_DEADLINE_INFO}}` - 截止日期信息（如果有）
- `{{CUSTOM_STATS}}` - 快速统计（根据内容调整）
- `{{DOMAIN_SECTION_TITLE}}` - 领域章节标题
- `{{DOMAIN_PROGRESS_TABLE}}` - 进度表格（根据内容结构生成）
- `{{DETAILED_TOPICS_SECTIONS}}` - 详细的主题章节（根据实际内容填充）
- `{{CUSTOM_STUDY_PLAN}}` - 学习计划（基于时间线和内容）
- `{{CUSTOM_MATERIALS_LIST}}` - 材料清单
- `{{CUSTOM_MILESTONES}}` - 里程碑

**关键**：这个文件应该反映实际内容的结构！

示例：
- 如果是书籍有12章 → 创建12个章节的追踪
- 如果是算法教程有 Easy/Medium/Hard 分类 → 按难度追踪
- 如果是考试有知识领域权重 → 按领域追踪，包含权重信息

#### 4.6 复制 SESSION-TEMPLATE.md

直接从 `assets/core-template/sessions/SESSION-TEMPLATE.md` 复制到新项目的 `/sessions/` 目录。

这个模板是通用的，不需要定制。

### 5. 生成总结报告

创建完项目后，向用户展示：

```markdown
✅ 学习项目已成功创建！

## 📁 项目位置
{完整路径}

## 📊 项目结构
{生成的目录树}

## 🎯 定制化说明

**识别的学习领域**：{领域名称}

**为什么选择这个结构**：
{解释选择的理由，包括：}
- 内容特点
- 学习目标
- 追踪维度的选择
- 额外添加的目录及原因

**如何使用**：
1. 进入项目目录：cd {路径}
2. 运行 Claude Code：claude-code
3. 开始提问，Claude 会自动记录你的学习历程

**关键文件**：
- `/progress/study-tracker.md` - 查看整体进度
- `/sessions/SESSION-TEMPLATE.md` - 会话记录模板
- `/anki-cards/` - Anki 卡片存储目录
- `/materials/` - 学习材料（如果提供了 URL）
- `CLAUDE.md` - AI 导师指令（已根据{领域}定制）

{如果有获取材料，添加以下内容：}
**学习材料**：
- 已从 {URL} 获取 {数量} 个页面的内容
- 查看 `/materials/README.md` 了解完整的材料列表
- Claude 会在回答问题时自动引用这些材料
{如果有失败链接，添加：}
- ⚠️ 部分链接获取失败，详见 `/materials/failed-links.md`

**Anki 集成**：
- Claude 会在学习过程中自动生成 Anki 卡片
- 卡片保存在 `/anki-cards/YYYY-MM-DD/cards.md`
- 使用 Obsidian + Obsidian_to_Anki 插件同步到 Anki
- 详见项目中的 `/anki-cards/anki-config.md`

## 💡 下一步

直接在这个目录中与我对话开始学习，或者查看 README.md 了解更多使用方法。
```

## 领域定制化指南

详细的领域定制化模式请参考：
- **`references/domain-templates.md`** - 包含各领域的完整定制化指南
- **`references/anki-integration.md`** - Anki 卡片集成完整指南

关键领域包括：
- 投资/理财
- 编程/算法
- 职业认证
- 语言学习
- 学术科目
- 技能/手艺

## Anki 卡片生成指南

所有学习项目都应包含 Anki 卡片功能。详见 `references/anki-integration.md`。

**关键要点**：

1. **卡片存储位置**：`/anki-cards/YYYY-MM-DD/cards.md`
2. **生成时机**：学生掌握新概念、重要数字/公式、对比区别时
3. **卡片格式**：
   - 标准版（英文 Anki）：使用 `Basic`、`Front:`、`Back:`
   - 中文版：使用 `问答题`、`正面:`、`背面:`
   - 填空题：使用 `{{c1::答案}}` 语法
4. **层级标签**：使用 `::` 创建层级（如 `投资::永久投资组合::第1章::核心概念`）
5. **Deck 指定**：在文件开头使用 `TARGET DECK: 项目名称`

**Claude 在生成卡片时应该**：
- 在教学过程中识别可制卡知识点
- 理解检查通过后自动生成卡片
- 保存到当日的卡片文件中
- 在会话记录中提及生成的卡片数量

## 质量检查清单

生成项目前，确认：

- [ ] 深入理解了内容主题和学习目标
- [ ] 选择了最合适的领域模板
- [ ] 根据具体内容调整了结构（不是死板套用）
- [ ] 创建了 `/anki-cards/` 目录
- [ ] 创建了 `/materials/` 目录
- [ ] 为所有空目录添加了 `.gitkeep` 文件
- [ ] 如果提供了 URL：
  - [ ] 使用 firecrawl MCP（如果可用）或 WebFetch 获取了内容
  - [ ] 递归获取了所有相关章节/页面的内容
  - [ ] 将内容保存为 markdown 文件到 `/materials/` 目录
  - [ ] 创建了 `/materials/README.md` 索引文件
  - [ ] 如果有失败的链接，创建了 `failed-links.md` 并添加了说明
  - [ ] 在 CLAUDE.md 中填充了 `{{MATERIALS_USAGE_INSTRUCTIONS}}` 变量（包含材料引用规则）
- [ ] 生成了 `anki-config.md` 配置文件
- [ ] study-tracker.md 反映了实际内容的章节/主题结构
- [ ] CLAUDE.md 包含了领域特定的导师指导
- [ ] README.md 清楚解释了为什么选择这个结构
- [ ] 所有变量都被正确替换
- [ ] 目录结构已创建
- [ ] 所有文件已生成

## 示例场景

### 示例 1：书籍《哈利布朗永久投资组合》

**分析**：
- 领域：投资/理财
- 内容：投资策略书籍
- 目标：理解并可能应用投资策略

**定制化**：
- 添加 `/portfolio/` 目录用于追踪实际投资组合
- 添加 `/strategy-notes/` 用于记录策略洞察
- CLAUDE.md 设置为投资顾问角色
- study-tracker.md 按书籍章节追踪，增加"投资组合表现"维度

### 示例 2：URL https://labuladong.online/zh/algo/intro/quick-learning-plan

**分析**：
- 领域：编程/算法
- 内容：算法学习路径
- 目标：掌握算法面试技能

**内容获取**：
1. 使用 firecrawl MCP 获取主页面内容
2. 识别所有章节链接（如：数组篇、链表篇、二叉树篇等）
3. 并行获取所有章节内容
4. 保存为 `materials/main.md`、`materials/arrays.md`、`materials/linked-lists.md` 等
5. 创建 `materials/README.md` 索引所有材料
6. 在 CLAUDE.md 中添加材料引用规则

**定制化**：
- 添加 `/solutions/easy/medium/hard/` 目录按难度组织题解
- 添加 `/patterns/` 目录记录算法模式
- 添加 `/materials/` 目录存储获取的教程内容
- CLAUDE.md 设置为算法导师角色，包含材料引用指令
- study-tracker.md 按难度和模式追踪，包含 LeetCode 题号

## 常见问题

**Q: 如果 URL 内容获取失败怎么办？**
A:
1. 如果使用 firecrawl 失败，尝试降级到 WebFetch
2. 如果单个链接失败，记录到 `failed-links.md` 并继续获取其他链接
3. 如果主页面失败，回退到基于 URL 模式和你的知识进行合理推断
4. 在 `failed-links.md` 中详细说明失败原因和用户如何手动补充

**Q: 如果书籍太冷门，找不到信息怎么办？**
A: 请用户简要描述书籍主题和章节结构，基于描述生成项目。

**Q: 混合领域怎么处理？**
A: 识别主要领域和次要领域，组合两者的定制化特点，并添加独特元素。例如"Python 金融分析" = 金融（主）+ 编程（次）+ 自定义 `/data-analysis/` 目录。

**Q: 用户想要的输出路径不存在怎么办？**
A: 确认父目录存在后创建子目录。如果父目录也不存在，提示用户提供有效路径。

## 重要提醒

1. **永远不要生成死板的结构** - 每个学习内容都是独特的
2. **深入分析胜过快速生成** - 花时间理解内容
3. **解释你的选择** - 在 README.md 中说明为什么这样设计
4. **保持核心方法一致** - 苏格拉底教学法 + 会话追踪是所有项目的基础
5. **测试生成的路径** - 确保所有文件都正确创建
