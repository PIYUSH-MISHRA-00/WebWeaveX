# Contributing to WebWeaveX

Thanks for your interest in improving WebWeaveX. This project aims to be a production-grade, open-source web intelligence platform, and we value high-quality contributions.

## Development Setup

Prerequisites:
- Git
- Python 3.11+
- Node.js 18+ (for Playwright, website, and JS tooling)
- Java 17+ (for JVM SDKs)
- Dart 3+ (for Dart SDK)

Setup steps:
1. Clone the repo.
2. Create a Python virtual environment.
3. Install tooling as it becomes available in each subproject.
4. Optional: enable pre-commit hooks.

Example:
```bash
git clone https://github.com/PIYUSH-MISHRA-00/WebWeaveX
cd WebWeaveX
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
```

## Branch Strategy

- `main` is the default branch and always kept in a releasable state.
- Create short-lived branches for work. Use `phase-X/<topic>` or `feature/<topic>`.
- Keep branches focused and avoid mixing unrelated changes.

## Pull Request Workflow

1. Create a branch from `main`.
2. Implement changes with tests and documentation.
3. Run lint and tests locally.
4. Open a PR and fill out the PR template.
5. Address review feedback and keep the PR up to date.

## Code Style Rules

- Python: follow PEP 8, prefer type hints, and keep functions small and testable.
- JavaScript/TypeScript: follow standard ESLint and Prettier conventions once configured.
- Java/Kotlin: follow standard formatter rules and keep APIs consistent across SDKs.
- Markdown/YAML: use clear headings, avoid long lines where practical, and keep formatting consistent.

## Commit Message Format

All commits must use:

```
phase-X: description
```

Example:
```
phase-1: implement core crawler engine
```
