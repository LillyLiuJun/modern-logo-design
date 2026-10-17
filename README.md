# Modern Logo Methodology

为产品设计现代 logo 的 skill：**先骨架，后颜色**。

```
阶段 0    环境准备        检查图像 API
阶段 1    信息收集        产品名、品类、想表达什么、标志类型
阶段 2    单色骨架矩阵    推导 3–4 个方向 → 单色出图 → 对照页
阶段 3    选定与微调      诊断 → 局部调整 → 锁定 1 个骨架
阶段 3.5  SVG 重绘        Claude 把骨架重绘成精确矢量（推荐）
阶段 4    上色与交付      色彩诊断 → 角色分配 → A/B/C 三种范式 → App 图标预览
```

安装后直接对 Claude 说「帮我给 XX 设计一个 logo」即可开始。
出图支持三家图像模型：**Gemini（Nano Banana）**、**ChatGPT（OpenAI 图像模型）**、**豆包（火山方舟 Seedream）**。

## 安装

把整个文件夹放到 skills 目录：

- macOS / Linux：`~/.claude/skills/modern-logo-methodology`
- Windows：`%USERPROFILE%\.claude\skills\modern-logo-methodology`

上传到 GitHub 后也可以用：
```bash
git clone <你的仓库地址> ~/.claude/skills/modern-logo-methodology
```

然后安装依赖、生成配置文件：
```bash
cd ~/.claude/skills/modern-logo-methodology
pip install -r requirements.txt
cp .env.example .env
```

## API Configuration

在 `.env` 里先选默认用哪一家，再填那一家的配置。**只需要填你要用的那一家。**

```
IMAGE_PROVIDER=gemini      # gemini / openai / doubao
```

### Gemini（Nano Banana）

官方接口：
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.1-flash-image-preview
```

第三方中转：
```
GEMINI_API_KEY=your_api_key_here
GEMINI_API_BASE_URL=https://api.example.com
GEMINI_MODEL=gemini-3.1-flash-image-preview
```

### ChatGPT（OpenAI 图像模型）

官方接口：
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-image-2
```

第三方中转：
```
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE_URL=https://api.example.com/v1
OPENAI_MODEL=gpt-image-2
```

### 豆包（火山方舟 Seedream）

先在火山方舟控制台开通 Seedream 模型，并在「API Key 管理」创建 key。

官方接口：
```
DOUBAO_API_KEY=your_api_key_here
DOUBAO_MODEL=doubao-seedream-4-0-250828
```

第三方中转：
```
DOUBAO_API_KEY=your_api_key_here
DOUBAO_API_BASE_URL=https://api.example.com/api/v3
DOUBAO_MODEL=doubao-seedream-4-0-250828
```

`DOUBAO_MODEL` 填你在控制台已开通的模型 ID；Seedream 4.5、5.0 等更新版本的 ID 以控制台显示为准。

### 中转地址怎么填

填服务商文档给的地址。OpenAI 中转一般以 `/v1` 结尾，豆包中转一般以 `/api/v3` 结尾，Gemini 中转按服务商说明填写。

### 检查配置

```bash
python scripts/check_env.py           # 检查当前选择的模型，并在线验证 key（不出图、不花生图额度）
python scripts/check_env.py --all     # 查看三家的配置状态
```

看到「环境就绪」就可以用了。豆包没有不出图的验证接口，第一次出图时才会验证 key。

### 其他字段

| 字段 | 说明 |
|---|---|
| `LOGO_OUTPUT_DIR` | 图片保存目录，默认 skill 目录下的 `output/` |

`.env` 已写进 `.gitignore`，不会被提交。

## 出图

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

## 其他脚本

```bash
# 对照页：图 + 设计阐述 + 中英文提示词
python scripts/build_review.py --names A1 B1 C1 --title "名称 · 骨架第 1 轮" --out output/round1.html

# SVG：渲染并与原图对比 / 按图层精确上色（不调用 API）
python scripts/render_svg.py output/A3.svg --source output/A3.png --name A3-svg
python scripts/render_svg.py output/A3.svg --name A3-c1 --colors "skeleton=#17120C,focus=#FF7622,bg=#FAF7F2"

# 色彩诊断：明度、彩度、冷暖、两两对比度、能否做渐变（不调用 API）
python scripts/color_check.py "#211811" "#FFF5EF" "#FF7622"

# App 图标预览：浅色 / 深色背景，180 / 64 / 32 / 16px（本地合成，不调用 API）
python scripts/make_preview.py output/A1.png
```

## 目录

```
modern-logo-methodology/
├── SKILL.md                    # 流程（阶段 0–4）
├── assets/
│   └── example_svg_s_office.svg  # SVG 重绘示例
├── README.md
├── .env.example                # API 配置模板
├── .gitignore
├── requirements.txt
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
