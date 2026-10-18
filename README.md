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

> 💡 **使用建议**：
> - **提示词推导**：建议使用 Gemini 系列模型作为对话 Agent，其生成的提示词在空间与意象表达上通常更有想象力。
> - **下游出图**：支持 Gemini、ChatGPT、豆包等图像模型（配置时选择对应的接口类型即可）。

## 快速开始

1. 按下面的步骤安装并配置 API（约 2 分钟）。
2. 打开 Claude Code，直接说：

   > 帮我给「XX」设计一个 logo

3. 看到「环境就绪」后，skill 会引导你走完整个流程。

## 安装

**1. 获取代码**

放到 Claude 的 skills 目录（macOS / Linux 为 `~/.claude/skills/`，Windows 为 `%USERPROFILE%\.claude\skills\`）。

仓库是私有的，克隆前需要已登录 GitHub。推荐用 `gh`：

```bash
gh auth login        # 已登录可跳过
gh repo clone LillyLiuJun/modern-logo-design ~/.claude/skills/modern-logo-design
```

或者直接用 git（需要有该仓库的访问权限）：

```bash
git clone https://github.com/LillyLiuJun/modern-logo-design.git ~/.claude/skills/modern-logo-design
```

**2. 安装依赖，生成配置文件**

```bash
cd ~/.claude/skills/modern-logo-design
pip install -r requirements.txt
cp .env.example .env
```

**3. 填写 API，检查配置**（见下一节）

## 配置 API

编辑 `.env`：先用 `IMAGE_PROVIDER` 选默认模型，再只填那一家的配置。

| 模型 | `IMAGE_PROVIDER` | 必填 | 可选 | 默认模型 |
|---|---|---|---|---|
| Gemini（Nano Banana） | `gemini` | `GEMINI_API_KEY` | `GEMINI_API_BASE_URL`、`GEMINI_MODEL` | `gemini-3.1-flash-image-preview` |
| ChatGPT（OpenAI） | `openai` | `OPENAI_API_KEY` | `OPENAI_API_BASE_URL`、`OPENAI_MODEL` | `gpt-image-2` |
| 豆包（Seedream） | `doubao` | `DOUBAO_API_KEY` | `DOUBAO_API_BASE_URL`、`DOUBAO_MODEL` | `doubao-seedream-4-0-250828` |

最小示例（以 Gemini 为例）：

```ini
IMAGE_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here
```

**用第三方中转**：把 `*_API_BASE_URL` 填成服务商给的地址。OpenAI 中转一般以 `/v1` 结尾，豆包中转一般以 `/api/v3` 结尾，Gemini 中转按服务商说明填写。留空则使用官方地址。

**豆包注意**：先在火山方舟控制台开通 Seedream 模型，并在「API Key 管理」创建 key。`DOUBAO_MODEL` 填你已开通的模型 ID，更新版本（4.5、5.0 等）以控制台显示为准。

**其他字段**：`LOGO_OUTPUT_DIR` 设置图片保存目录，默认是 skill 目录下的 `output/`。

`.env` 与 `output/` 已写进 `.gitignore`，不会被提交。

### 检查配置

```bash
python scripts/check_env.py           # 检查当前选择的模型，并在线验证 key（不出图、不花生图额度）
python scripts/check_env.py --all     # 查看三家的配置状态
```

看到「环境就绪」就可以用了。豆包没有不出图的验证接口，第一次出图时才会验证 key。

## 脚本用法

平时由 Claude 自动调用，需要手动操作时可参考下面的命令。

### 出图

```bash
# 骨架阶段：只用文字出图
python scripts/generate_image.py --name A1 --prompt-file A1.en.txt --prompt-zh-file A1.zh.txt

# 上色阶段：传入已确认的骨架图，锁定形状
python scripts/generate_image.py --name A1-color --stage color --ref output/A1.png --prompt-file c.en.txt

# 临时换一家模型
python scripts/generate_image.py --provider doubao --name A1 --prompt "..."

# 只看请求内容，不调用 API
python scripts/generate_image.py --dry-run --prompt "..."
```

每张图旁边会生成同名 `.json`，记录中英文提示词、模型和参考图。

### 其他工具（均不调用 API）

```bash
# 对照页：图 + 设计阐述 + 中英文提示词（build_review.py 只拼页面，不出图）
python scripts/build_review.py --names A1 B1 C1 --title "名称 · 骨架第 1 轮" --out output/round1.html

# SVG：渲染并与原图对比 / 按图层精确上色
python scripts/render_svg.py output/A3.svg --source output/A3.png --name A3-svg
python scripts/render_svg.py output/A3.svg --name A3-c1 --colors "skeleton=#17120C,focus=#FF7622,bg=#FAF7F2"

# 色彩诊断：明度、彩度、冷暖、两两对比度、能否做渐变
python scripts/color_check.py "#211811" "#FFF5EF" "#FF7622"

# App 图标预览：浅色 / 深色背景，180 / 64 / 32 / 16px
python scripts/make_preview.py output/A1.png
```

## 常见问题

| 现象 | 处理 |
|---|---|
| `check_env.py` 提示 key 无效 | 确认填的是所选 `IMAGE_PROVIDER` 对应那一家的 key，且 `.env` 在 skill 根目录 |
| 用中转地址报 404 | 检查地址后缀：OpenAI 要 `/v1`，豆包要 `/api/v3` |
| 豆包报模型未开通 | 到火山方舟控制台开通模型，并把 `DOUBAO_MODEL` 改成已开通的 ID |
| 克隆提示无权限 | 仓库是私有的，先执行 `gh auth login`，并确认账号有访问权限 |

## 目录

```
modern-logo-design/
├── SKILL.md                    # 流程（阶段 0–4）
├── README.md / README.en.md    # 中文 / 英文说明
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
