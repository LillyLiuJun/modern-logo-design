# Modern Logo Design

[English](README.md) | **简体中文**

为产品设计现代 logo 的 skill：**先骨架，后颜色**。将感性、发散、具象的品牌需求，翻译为具备包豪斯必然性、现代数学秩序、高阶曲率张力与操作系统级质感的工程级矢量 logo。

<table align="center">
  <tr>
    <td align="center" width="25%">
      <img src="assets/showcase/poplex.png" width="150" alt="Poplex logo：字母 P 与嫩芽"><br>
      <sub>Poplex<br>字母 + 嫩芽</sub>
    </td>
    <td align="center" width="25%">
      <img src="assets/showcase/s-negative-space.png" width="150" alt="圆角方块里的负空间 S"><br>
      <sub>圆角方块<br>负空间 S</sub>
    </td>
    <td align="center" width="25%">
      <img src="assets/showcase/tree-light.png" width="150" alt="浅底大树标"><br>
      <sub>大树标<br>浅底</sub>
    </td>
    <td align="center" width="25%">
      <img src="assets/showcase/tree-reversed.png" width="150" alt="深底反白大树标"><br>
      <sub>大树标<br>深底反白</sub>
    </td>
  </tr>
</table>

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

> 💡 **提示**：写提示词的对话 Agent 如果在 Claude 和 Gemini 之间犹豫，我们个人更推荐 Gemini，它的提示词在空间和意象上更有想象力。

## 快速开始

### 1. 安装

把下面这段话发给 Claude Code（或其他支持 skill 的 Agent）：

> 帮我把 https://github.com/LillyLiuJun/modern-logo-design 安装为 skill，放到 ~/.claude/skills/modern-logo-design，装好依赖，并用 .env.example 生成 .env。然后告诉我要打开哪个文件、填哪个 Key。不要让我把 Key 贴到对话里。

然后打开 `.env`，设置 `IMAGE_PROVIDER`（`gemini`、`openai` 或 `doubao`），填对应的 Key（`GEMINI_API_KEY`、`OPENAI_API_KEY` 或 `DOUBAO_API_KEY`）。其余字段不用动，用第三方中转时才需要另外填 `*_API_BASE_URL`。

<details>
<summary>手动安装</summary>

```bash
git clone https://github.com/LillyLiuJun/modern-logo-design.git ~/.claude/skills/modern-logo-design
cd ~/.claude/skills/modern-logo-design
pip install -r requirements.txt
cp .env.example .env
```

</details>

### 2. 开始使用

告诉你的 Agent 要做什么（以 Poplex 为例）：

> 帮我给「Poplex」设计一个 logo：
> 
> - **名称**：Poplex（首字母大写）。
> - **品类与场景**：iOS 英语学习 App，面向想把英语用进日常生活的成年人；一句话定位是 *build language from your life*，把生活里遇到的内容变成自己的英语积累，每天高频打开。
> - **想传达什么**：生长、积累、安静克制、有书卷的编辑感。避免打勾、对话气泡、字母 A–Z、地球、灯泡这类学习 App 的陈旧隐喻。
> - **标志类型**：纯符号，想先看看这类「生长」意象；用字母 P 和嫩芽组成的元素。
> - **已有素材（可选）**：附上几张 App 界面截图，以及现有的 P + 墨点标记，作为调性参考而不是照抄。
> - **颜色（可选）**：例如暖纸底 `#FBF8F5`、橙色 `#FF7622`、墨色 `#2A2320`。出图时会用上；如果颜色干扰了形状判断，就退回单色，在阶段 4 再优化颜色。

这些对应 skill 的「阶段 1：信息收集」。没想好的写「不确定，由你推荐」。之后 skill 会推导 3–4 个方向，每轮生成一个 HTML 对照页。

## 如何逼近你想要的感觉

好 Logo 很少一轮就抽中，它是「推导骨架 → 诊断问题 → 每次只改一处」逐步收敛的。两个方法：

**1. 发参考图，并说清你认可它的哪一点。**
发 1–2 张调性对的 Logo 截图，不要只说「参考这个」，而是点名认可的部分：咬合的线条、挺拔的超椭圆转角、大留白。再让 AI 借用其中的几何关系，而不是照搬图案。

**2. 用物理语言描述问题，不用品味词。**
「不够高级」没法让 AI 调参数。参考 `references/skeleton_axioms.md`，从这几个维度说：

- **松 / 紧**：字怀或切缝是太挤还是太散？
- **粗 / 细**：线条是单薄如发丝，还是笨重？
- **轻 / 重**：重心偏高还是偏低？
- **硬 / 软**：转角是机械的，还是松垮的？

例如：「下半部分太沉，把间距拉大 15%，转角做微倒角。」

## 目录

```
modern-logo-design/
├── SKILL.md                    # 流程（阶段 0–4）
├── README.md / README.zh-CN.md # 英文 / 中文说明
├── LICENSE                     # MIT 开源协议
├── .env.example                # API 配置模板
├── requirements.txt
├── assets/
│   ├── example_svg_s_office.svg  # SVG 重绘示例
│   └── showcase/                 # README 顶部展示的 logo
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

## 参与贡献

欢迎提 issue 和 Pull Request，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 开源协议

本项目基于 [MIT License](LICENSE) 开源。

