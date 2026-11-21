# ai pull request review

CodeGuardAI is an AI‑powered assistant that automatically analyzes pull‑requests, flagging bugs, security vulnerabilities, and bad coding practices. It provides an **ai pull request review** experience that helps open‑source maintainers and development teams catch issues early, improve code quality, and accelerate continuous integration workflows.

## Problem

Maintainers of open‑source projects and development teams often spend valuable time manually reviewing pull‑requests. Manual reviews can miss subtle bugs, security flaws, or deviations from coding best practices, especially in fast‑moving repositories. Existing tools either provide generic linting or expensive enterprise‑grade scanning, leaving a gap for a lightweight, context‑aware solution tailored to small and medium projects.

## Solution

CodeGuardAI brings an ultra‑precise, context‑aware AI review directly into your pull‑request workflow. By analyzing the diff, the surrounding codebase, and project conventions, it delivers actionable feedback on bugs, vulnerability detection, and coding best practices. The service integrates seamlessly with GitHub via webhooks, runs as a lightweight FastAPI service, and can be deployed with Docker.

## Who is it for

- **Open‑source maintainers** who need fast, reliable feedback on incoming contributions.
- **Development teams** looking to automate code analysis as part of their CI/CD pipeline.
- **DevOps engineers** seeking a plug‑and‑play AI pull request review tool without complex setup.

## Features

- **AI‑driven code analysis** that understands the context of each pull‑request diff.
- **Bug detection** with clear explanations and suggested fixes.
- **Security scanning** to highlight potential vulnerabilities and insecure patterns.
- **Style checks** such as line length and stray debug prints.
- **GitHub webhook integration** for automatic PR checks.
- **REST API** exposing `/health` and `/review` endpoints.
- **Docker support** for easy deployment in any environment.

## Use cases

- **Pre‑merge validation** – automatically run a review when a contributor opens a PR, catching issues before they reach the main branch.
- **Continuous integration** – embed CodeGuardAI in CI pipelines to enforce quality gates on every build.
- **Security audits** – scan new contributions for known vulnerability patterns without manual effort.
- **Mentorship** – provide new contributors with instant feedback, helping them learn coding best practices.

## Installation and configuration

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

For Docker users:

```bash
docker build -t codeguardai .
docker run -p 8000:8000 codeguardai
```

The API runs on port 8000 and provides the following endpoints:

- `GET /health` – returns service status.
- `POST /review` – accepts a JSON payload describing a pull‑request diff and returns detected issues.

## Usage examples

### Quick API test

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

### Review a pull request diff

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Add new feature",
    "description": "",
    "files": [
      {
        "filename": "app.py",
        "added_lines": ["def foo():", "    print(\"debug\")", "    api_key = \"ABCD1234EFGH5678IJKL\""],
        "removed_lines": []
      }
    ]
  }'
```

The response will list any security findings (e.g., hard‑coded secret) and style issues (e.g., debug print, line too long).

## Limitations

- The AI model currently focuses on Python, JavaScript, and TypeScript files as defined in the demo validator.
- Real‑time analysis depends on the size of the diff; very large PRs may take longer to process.
- The demo uses simple regex‑based checks and does not provide deep static analysis or full project context.
