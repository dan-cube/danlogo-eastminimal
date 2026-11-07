---
name: danlogo-eastminimal
description: >-
  DanLogo · East Minimal 东方极简：让 AI 工具（Claude、Codex 等）以老子“无之用”的东方思想为根，做成套的 logo 与品牌标志体系——空与白、以少见多、让物性说话；
  从品牌身上找出人人见过却没人注意的东西，画成一个有外形、有面的图形（不是字的变体），用最少的形承载最深的意思，图形与中英文定制字同源，留出空间让人自己完成理解。
  按九个阶段从简报做到交付：简报 → 概念（每轮 5 套）→ 原型（每个概念 ≥3 套）→ 图形精修 → 定稿（定制字 + 配色）→ 体系 → 场景 → 提案 → 总结，含后期制作与交付文件包。
  Use this skill when the user wants to design, redesign, refine, extend or present a logo, wordmark, 标志, 字标, 中英文组合标,
  品牌视觉, VI or brand identity in an East-Asian minimalist spirit — 东方极简, 东方美学, 留白, 空, 白, 禅意, 无印良品, 原研哉, 克制, 高级感 —
  when they name danlogo-eastminimal, or when they continue a project whose decisions.md names it. For a logo request that names
  no style, use it unless another installed danlogo style fits better; if several danlogo styles are installed, ask the user which one first.
---

# DanLogo · East Minimal 东方极简

> 用最少的形，承载最深的意思；留出空间，让人自己完成理解。

danlogo 系列的东方极简方向。它规定**气质和质量**，不规定形状、颜色或工艺。它以老子“无之用”的东方思想为根，经由八大山人的笔简意足、枯山水的以少见多这些东方艺术传统转化为设计方法，并参照原研哉、Dieter Rams、无印良品等当代艺术设计理念。它从 EonPoint 亿触点“一实一空”方案反向拆解而来（`cases/`），但每个新品牌都要从自己身上长出新的形——做出来的标志气质相通，却不会都长成同一个样子。

## 先读

开始任何项目之前，按顺序读完风格三章：

1. `references/philosophy.md` —— 思想坐标与十条设计思想：为什么这样设计
2. `references/style-dna.md` —— 九条风格基因、旋钮与试金石：看起来是什么气质
3. `references/creative-methods.md` —— 七种创意方法与防同质化：每次怎么想出新的

`references/exemplars.md`（参照作品）和 `cases/index.md`（已用过的母题）**等第 2 阶段列完候选母题再读**，用它们划掉惯性答案和撞题的母题——先读会被它们带着走。完整案例只在需要参照“做到什么程度”时读，并且只借方法、不借形式。其余文件在对应阶段读（见下表）。

## 三层要求

| 层 | 内容 | 能否改变 |
|---|---|---|
| 质量关卡（系列共用） | `references/quality-gates.md` | 每个项目都必须通过 |
| 风格基因（本风格） | `style-dna.md` 九条 + `philosophy.md` 十条自检 | 默认遵守；用户明确要求调整时照做，并记入 decisions.md |
| 创意自由区 | 母题、造型语言、力度、温度、色彩、材料、构图 | 每个项目重新推导；至少两个“旋钮”与所有已有案例明显不同 |

三句提醒：
- **首先是一个图形。** 标志第一眼要读成一个东西或一个画面，有外形、有面；不是字、字母、标点的变体，也不是几根线搭成的记号（`quality-gates.md`“怎么判断图形感”）。
- **按气质判断，不按元素判断。** 案例里的点、圆、句号、某种红、盲压，都是那个品牌的答案，不是本风格的规定。
- **克制不等于平淡。** 元素少，但要有强烈的存在感和态度。

**分工**：本 skill 守住流程、想法、风险和底线，每轮交出方向清楚、取舍写明的原型；形的分寸——黑白比例、签名大小、外形个性——在第 4 阶段与用户一起打磨，不由 AI 独自定稿。

## 九个阶段

细则、编号规则、出口条件见 `references/workflow.md`。每个阶段都以用户的明确确认结束；用户可以随时回退、增加、修改、合并。

| 阶段 | 做什么 | 每轮产出 | 读 |
|---|---|---|---|
| 1 简报 | 用户提供信息；AI 一次性追问缺口（≤10 问） | 简报卡 | `workflow.md`、`philosophy.md` 第 1 条 |
| 2 概念 | 挖母题，列完候选再读示范与案例索引 | **5 张概念卡**（每张配黑白速写），可改、可加、可合并 | `creative-methods.md`、`exemplars.md`、`cases/index.md` |
| 3 原型 | 每个锁定概念发散图形；只做形，只用黑白 | **每个概念 ≥3 个原型** + 初步查重 | `style-dna.md`、`craft.md` |
| 4 图形 | 精修：构造规则、视觉修正、小尺寸版、构造图 | 精修图形 | `craft.md`、`quality-gates.md` |
| 5 定稿 | 定制字与配色一起做 | 每个图形 2–3 套“字 + 色”组合 + 完整查重 | `craft.md`、`style-dna.md` |
| 6 体系 | 组合、变色、留白、最小尺寸、错误用法、动态 | SVG / PNG 全套 | `deliverables.md` |
| 7 场景 | 按行业选 6–10 个场景 | 场景示意 | `deliverables.md` |
| 8 提案 | 提报文档 + 演讲备注 + 源文件包 + 查重复查 | 提案 | `deliverables.md`、`adapters/` |
| 9 总结 | 主动询问是否用这个项目优化 skill | 修改建议，用户批准后写入 | `workflow.md` 第 9 节 |

## 贯穿全程

- **项目存档**：每个项目一个文件夹和一份 `decisions.md`（第一行写 `skill: danlogo-eastminimal v<版本>`），记录每轮展示了什么、用户原话、锁定和否定了什么。接手已有项目先读它。
- **黑白先行**：第 5 阶段之前不上色。
- **被否就退回，不加东西**：换母题或换原型，不在原图上加装饰。
- **查重三次**：原型初查、定稿全查、提案前复查（`quality-gates.md`）。
- **亲眼看渲染图**：判断好不好看，一律基于渲染出的图片，包括 16 px 小图。
- **沟通**：用用户的语言。每轮先一句话说做了什么，再编号列方案和一句话理念，给一个推荐和理由，问锁定、修改还是继续。简短反馈先查 `references/feedback-playbook.md`。
- **客户资料只放在项目文件夹里**，不写进 skill。

## 多个 danlogo 风格并存时

用户点名了某个风格，就用那个 skill。项目的 `decisions.md` 写了用哪个 skill，就沿用。都没有指定、又装了多个 danlogo 风格时，先列出已安装的风格，请用户选，再开始。

## 工具与文件

- `scripts/`：通用工具——几何与 SVG 生成（`geom.py`）、多图对比审看图（`sheet.py`）、SVG 转 PNG（`render.sh`）、图形感与辨识度审看板（`review.py`）。说明见 `scripts/README.md`。使用时复制到项目的 `src/`。
- `examples/eonpoint/src/`：EonPoint 案例的完整生成代码。学它的工程写法（参数组织、批量导出、构造图、动态帧），不要复用它的造型和字形。
- `adapters/for-claude.md`、`adapters/for-codex.md`：不同 AI 工具在看图、做演示文稿、预览网页上的差异。
- `evals/briefs.md`：用于检验本 skill 不会把所有品牌做成同一个样子的测试简报。

`references/` 中带 `danlogo-core` 标记的五个文件（workflow、quality-gates、craft、deliverables、feedback-playbook）是 danlogo 系列共用章节，所有风格保持一致；本风格专属的是 philosophy、style-dna、creative-methods 三章。
