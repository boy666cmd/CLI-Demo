# 作业提交材料

## 提交信息模板（复制后填写）

```
姓名：[你的姓名]
联系方式：[手机号 / 邮箱]

GitHub 仓库：https://github.com/[用户名]/resume-cli-demo
演示视频：[视频链接，如 B站/腾讯会议/飞书]
```

---

## GitHub 上传步骤

```powershell
cd "D:\Projects\AICoding\CLI Demo"
git init
git add .
git status
git commit -m "feat: AI resume parsing CLI demo"
```

在 GitHub 创建 **Public** 仓库后：

```powershell
git remote add origin https://github.com/[用户名]/resume-cli-demo.git
git branch -M main
git push -u origin main
```

**提交前确认：**
- [ ] 没有 `.env` 文件（只有 `.env.example`）
- [ ] 没有 `venv/` 目录被提交
- [ ] README.md 完整

---

## 演示视频口播稿（约 3 分钟）

见下方完整脚本，录屏时打开终端 + 编辑器并排展示。

---

## 演示命令清单

```powershell
cd "D:\Projects\AICoding\CLI Demo"
pip install -e ".[dev]"
python scripts/generate_sample_pdf.py
python -m resume_cli --help
python -m resume_cli parse samples/resume.pdf
python -m resume_cli extract samples/resume.pdf --mock
python -m resume_cli score samples/resume.pdf --jd samples/sample_jd.txt --mock
python -m pytest -v
```
