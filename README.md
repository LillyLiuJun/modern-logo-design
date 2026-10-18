# Modern Logo Design

**简体中文** | [English](README.en.md)

为产品设计现代 logo 的 Claude skill：**先骨架，后颜色**。将感性、发散、具象的品牌需求，翻译为具备包豪斯必然性、现代数学秩序、高阶曲率张力与操作系统级质感的工程级矢量 logo。

<p align="center">
  <img src="assets/example_svg_s_office.svg" width="240" alt="示例：圆角方块 + 负空间 S">
</p>
<p align="center"><sub>示例：圆角方块 + 负空间 S，由 skill 在阶段 3.5 重绘为精确矢量</sub></p>

## 核心价值主张：Logo 的固有法则

Logo 不是画作或装饰贴纸，而是一种拥有固有结构与数学规律的严苛设计对象。

本 Skill 将感性、发散的品牌直觉，转化为**所有合格 Logo 成立的必然原则**：

- **包豪斯必然性**：多一笔是冗余，少一笔则解体。意象即主体轮廓，拒绝外挂装饰贴花。
- **现代数学秩序**：主干、圆弧与间距共享基准模数 $w$，基于严密的布尔几何构造。
- **高阶曲率张力（G²）**：超椭圆连续曲率与紧绷弧线，消除机械死圆角的生硬接头。
- **操作系统级质感**：**先骨架，后颜色**。单色形态必须独立成立，16px 极小尺寸下锐利不溃烂。

## 它做什么

你给出产品背景，skill 帮你推导意象、出图、挑选、精修、上色，最后交付可用的矢量 logo 和 App 图标预览。每个阶段结束都由你确认再进入下一步，随时可以退回。

```
阶段 0    环境准备        检查图像 API
阶段 1    信息收集        产品名、品类、想表达什么、标志类型
阶段 2    单色骨架矩阵    推导 3–4 个方向 → 单色出图 → 对照页
阶段 3    选定与微调      诊断 → 局部调整 → 锁定 1 个骨架
阶段 3.5  SVG 重绘        Claude 把骨架重绘成精确矢量（推荐）
阶段 4    上色与交付      色彩诊断 → 角色分配 → A/B/C 三种范式 → App 图标预览
```

出图支持三家图像模型：**Gemini（Nano Banana）**、**ChatGPT（OpenAI 图像模型）**、**豆包（火山方舟 Seedream）**。

> 💡 **模型建议（个人使用偏好）**：
> - **提示词推导**：如果你在 Claude 和 Gemini 模型之间犹豫，个人更倾向推荐使用 Gemini 系列模型作为对话 Agent，某种程度其生成的提示词在空间与意象表达上通常更有想象力。
> - **下游出图**：支持 Gemini、ChatGPT、豆包等图像模型（配置时选择对应的接口类型即可）。

## 如何逼近你想要的感觉（迭代技巧）

好 Logo 几乎不可能一轮生成抽中，它是一个「推导骨架 → 诊断问题 → 控制变量微调」逐步收敛的过程。如果生成的方案离预期有差距，推荐使用以下两种方法：

### 方法一：截屏参考 Logo，明确指出你认可的具体细节
发 1~2 张你觉得调性对的现有 Logo 截图给 AI。**切忌只说“参考这个”**，而是明确拆解出你认可的具体元素：
- “我认可它两根线条咬合形成的通透感”
- “我喜欢它这个外圈超椭圆转角的挺拔曲率”
- “我认可它整体的大留白比例，不要太满”
告诉 AI：“请提取参考图中的这一几何动势，但不要照搬其具体图案。”让 AI 借力成熟标志的形式结构，而不是表面临摹。

### 方法二：用「低维物理语言」描述想法，避免抽象品味词
当对结果不满意时，尽量避免使用“不够高级”、“差点意思”、“太土”等模糊高维词（AI 无法据此精准修改参数）。
参考 `references/skeleton_axioms.md`（骨架公理），把感受拆解为可感知的物理维度：
- **松 / 紧**：内部字怀或切缝是太挤还是太散？
- **粗 / 细**：主干线宽是显得单薄（发丝线），还是笨重（色块堆积）？
- **轻 / 重**：视觉重心是偏高显得飘，还是偏低显得沉？
- **硬 / 软**：转角是机械死直角（需要 G² 连续曲率平滑），还是像随手画的一样泄气（需要增加张力）？
直接用物理语言提要求（如：“下半部分太沉，请将底部间距拉大 15%；转角过硬，请做微倒角处理”）。描述问题时，**用低维物理语言**，不用「不好看」「不高级」这类品味词。

## 快速开始

### 1. 安装与配置（约 1 分钟）

```bash
# 获取代码至 Claude skills 目录（私有仓库推荐 gh，也可直接 git clone）
gh repo clone LillyLiuJun/modern-logo-design ~/.claude/skills/modern-logo-design

# 安装依赖并生成配置文件
cd ~/.claude/skills/modern-logo-design
pip install -r requirements.txt
cp .env.example .env
```

编辑 `.env`：先用 `IMAGE_PROVIDER` 选默认模型（`gemini` / `openai` / `doubao`），填那一家的 Key（支持第三方中转地址）：

| 模型 | `IMAGE_PROVIDER` | 必填 Key | 可选参数（中转 / 自定义模型） |
|---|---|---|---|
| Gemini（Nano Banana） | `gemini` | `GEMINI_API_KEY` | `GEMINI_API_BASE_URL`、`GEMINI_MODEL` |
| ChatGPT（OpenAI） | `openai` | `OPENAI_API_KEY` | `OPENAI_API_BASE_URL`、`OPENAI_MODEL` |
| 豆包（Seedream） | `doubao` | `DOUBAO_API_KEY` | `DOUBAO_API_BASE_URL`、`DOUBAO_MODEL` |

验证配置（仅在线验 Key，不出图、不花额度）：
```bash
python scripts/check_env.py
```
看到「环境就绪」即可。

### 2. 开始使用

在 Agent 终端中使用（以 Poplex 为例）：

> 帮我给「Poplex」设计一个 logo：
> 
> - **名称**：Poplex（首字母大写）。
> - **品类与场景**：iOS 英语学习 App，面向想把英语用进日常生活的成年人；一句话定位是 *build language from your life*，把生活里遇到的内容变成自己的英语积累，每天高频打开。
> - **想传达什么**：生长、积累、安静克制、有书卷的编辑感。避免打勾、对话气泡、字母 A–Z、地球、灯泡这类学习 App 的陈旧隐喻。
> - **标志类型**：纯符号，想先看看这类「生长」意象；用字母 P 和嫩芽组成的元素。
> - **已有素材（可选）**：附上几张 App 界面截图，以及现有的 P + 墨点标记，作为调性参考而不是照抄。
> - **关于颜色**：可以不提。前期给了品牌色（例如暖纸底 `#FBF8F5`、品牌橙 `#FF7622`、墨色 `#2A2320`），出图时会用上；如果颜色干扰了形状判断、效果不好，就改回单色，或者在阶段 4 继续优化颜色。

上面 5 条正好对应 skill 的「阶段 1：信息收集」，一次性写全就不会被追问。哪条没想好可以直接写「不确定，由你推荐」。

Skill 收到后会自动推导 3–4 个截然不同的结构方向，进入骨架出图，并在每轮生成本地可交互的 HTML 对照页供你挑选与逐轮诊断。

## 目录

```
modern-logo-design/
├── SKILL.md                    # 流程（阶段 0–4）
├── README.md / README.en.md    # 中文 / 英文说明
├── LICENSE                     # MIT 开源协议
├── .env.example                # API 配置模板
├── requirements.txt
├── assets/
│   └── example_svg_s_office.svg  # SVG 重绘示例
├── references/
│   ├── skeleton_axioms.md      # 骨架公理：推导与诊断
│   ├── svg_redraw.md           # SVG 重绘：约定、步骤、对比、上色
│   ├── color_dressing.md       # 上色：诊断、角色、三种范式、检查
│   └── prompt_templates.md     # 中英文提示词模板
└── scripts/
    ├── _config.py              # 读取 .env
    ├── check_env.py            # 环境检查
    ├── generate_image.py       # 出图
    ├── build_review.py         # 对照页
    ├── render_svg.py           # SVG 渲染、对比、按图层上色
    ├── color_check.py          # 色彩诊断
    ├── make_preview.py         # App 图标预览
    └── providers/              # 各家模型的连接代码
        ├── gemini.py
        ├── openai_images.py
        └── doubao.py
```

## 开源协议

本项目基于 [MIT License](LICENSE) 开源。

