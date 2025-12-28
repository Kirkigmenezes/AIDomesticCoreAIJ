# Git Configuration Files for AI Platform SDK

## Overview
This directory contains Git configuration and CI/CD pipeline definitions for the AI Platform SDK.

## Contents

### GitHub Actions (.github/workflows/)
- **tests.yml** - Unit tests, coverage, and multi-OS compatibility
- **quality.yml** - Code quality, security, and documentation checks
- **pr.yml** - Pull request validation and checks
- **release.yml** - Build, test, and publish releases

### GitHub Templates (.github/ISSUE_TEMPLATE/)
- **bug_report.md** - Bug report template
- **feature_request.md** - Feature request template
- **pull_request.md** - Pull request template (in root)

### GitLab CI (.gitlab-ci.yml)
Complete CI/CD pipeline for GitLab including:
- Unit and integration tests
- Code quality checks (lint, type checking, security)
- Build distribution packages
- Docker image building
- Documentation deployment to GitLab Pages
- PyPI deployment

## Workflows

### On Push to main/develop
1. Run all tests across Python 3.9, 3.10, 3.11
2. Test on Ubuntu, Windows, macOS
3. Check code quality
4. Upload coverage to Codecov
5. Build distribution packages

### On Pull Request
1. Run tests
2. Code quality checks
3. Security scans
4. PR validation

### On Tag (Release)
1. Create GitHub release
2. Publish to PyPI
3. Build and push Docker image
4. Notify via Slack

## Local Setup

### Git Hooks
To set up pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Branch Protection Rules
Recommended settings for `main` branch:
- Require PR reviews (1-2 reviewers)
- Require status checks to pass:
  - tests (all Python versions/OS combinations)
  - code-quality
  - build
  - security
- Require branches to be up to date
- Dismiss stale review approvals
- Include administrators in restrictions

## Secrets Management

Required GitHub Secrets:
- `PYPI_API_TOKEN` - PyPI authentication token
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password
- `SLACK_WEBHOOK` - Slack webhook for notifications
- `CODECOV_TOKEN` - Codecov integration token (optional)

Required GitLab CI Variables (Settings > CI/CD > Variables):
- `PYPI_TOKEN` - PyPI authentication
- `REGISTRY_PASSWORD` - GitLab registry authentication

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for detailed contribution guidelines.

## Status Badges

Add these to README.md:

```markdown
[![Python Tests](https://github.com/sorydev/AIDomesticCoreAIJ/actions/workflows/tests.yml/badge.svg)](https://github.com/sorydev/AIDomesticCoreAIJ/actions)
[![Code Quality](https://github.com/sorydev/AIDomesticCoreAIJ/actions/workflows/quality.yml/badge.svg)](https://github.com/sorydev/AIDomesticCoreAIJ/actions)
[![codecov](https://codecov.io/gh/sorydev/AIDomesticCoreAIJ/branch/main/graph/badge.svg)](https://codecov.io/gh/sorydev/AIDomesticCoreAIJ)
```
