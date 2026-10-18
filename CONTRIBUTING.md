# 参与贡献 / Contributing

欢迎提 issue 和 Pull Request。Issues and pull requests are welcome.

## 提 issue

- **Bug**：说明你用的图像模型（Gemini / OpenAI / 豆包）、运行的命令、完整的报错。
- **建议**：说清楚想解决什么问题，比说清楚想怎么改更有用。
- **不要贴 API Key**。贴日志前先检查有没有 Key 或中转地址。

## 提 Pull Request

1. Fork 仓库，从 `main` 拉一个分支。
2. 改动尽量小，一个 PR 只做一件事。
3. 改了脚本：跑一遍 `python scripts/check_env.py`，并说明你测过哪些模型。
4. 改了流程或公理（`SKILL.md`、`references/`）：写清楚为什么改，最好附上改前、改后的出图对比。这个 skill 的规则来自实际出图的经验，没有出图依据的改动很难判断对错。
5. 中英文 README 要同步改。

## 不要提交

- `.env`、任何真实的 Key
- `output/`、`.venv/`（已在 `.gitignore` 里）
- 来源不明或有版权的 logo 图片

## 许可

提交代码即表示你同意以 [MIT License](LICENSE) 授权你的贡献。
