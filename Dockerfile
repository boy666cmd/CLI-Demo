FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml requirements.txt README.md ./
COPY resume_cli/ resume_cli/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["resume-cli"]
