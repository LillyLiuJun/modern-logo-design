# Contributing

Issues and pull requests are welcome.

## Filing an issue

- **Bug**: state the image provider you use (Gemini / OpenAI / Doubao), the command you ran and the full error.
- **Suggestion**: describe the problem you want to solve; that is more useful than describing how you would change it.
- **Never paste API keys.** Before pasting logs, check them for keys or relay addresses.

## Opening a pull request

1. Fork the repository and branch from `main`.
2. Keep changes small; one pull request, one thing.
3. If you changed a script: run `python scripts/check_env.py` and say which providers you tested.
4. If you changed the workflow or the axioms (`SKILL.md`, `references/`): explain why, ideally with before/after images. The rules of this skill come from experience with real generated images, so changes without that evidence are hard to judge.
5. Keep `README.md` and `README.zh-CN.md` in sync.

## Do not commit

- `.env` or any real key
- `output/` and `.venv/` (already in `.gitignore`)
- Logo images of unknown origin or under copyright

## License

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
