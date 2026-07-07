# 示例文件说明

## sample_jd.txt

示例岗位描述文件，可直接用于 `score` 命令：

```bash
resume-cli score <your_resume.pdf> --jd samples/sample_jd.txt --mock
```

## resume.pdf

请自行准备一份 PDF 简历用于测试。也可使用任意 PDF 文件替换 `<your_resume.pdf>`。

若需快速生成测试用 PDF，可运行：

```bash
python scripts/generate_sample_pdf.py
```

这会在 `samples/` 目录下生成 `resume.pdf`。
