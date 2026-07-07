.PHONY: install test parse extract score

install:
	pip install -e ".[dev]"

test:
	pytest -v

parse:
	resume-cli parse samples/resume.pdf

extract:
	resume-cli extract samples/resume.pdf --mock

score:
	resume-cli score samples/resume.pdf --jd samples/sample_jd.txt --mock
