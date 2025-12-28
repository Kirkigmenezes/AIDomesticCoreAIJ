# GitLab Configuration

## Overview
This directory contains GitLab-specific configuration files.

## Contents

### .gitlab-ci.yml
Main CI/CD pipeline definition with:
- Unit and integration tests
- Code quality checks
- Security scanning
- Docker image building
- Documentation deployment to GitLab Pages
- PyPI publishing

### CI/CD Variables
Configure in Settings → CI/CD → Variables:

```
PYPI_TOKEN      PyPI API token for package publishing
DOCKER_TOKEN    Docker authentication token
REGISTRY_PASSWORD GitLab registry authentication
```

## Running CI/CD Locally

### Using gitlab-runner

```bash
# Install gitlab-runner
# https://docs.gitlab.com/runner/install/

# Run specific job
gitlab-runner exec docker test:unit

# Run with variables
gitlab-runner exec docker test:unit -e PYPI_TOKEN=xxx
```

## Status

View pipeline status:
- **Main branch**: Latest stable version
- **Develop branch**: Development version
- **Tags**: Release versions

## Integration

- Automatic deployment on tag push
- Scheduled security scans
- Dependency scanning and updates
- Code coverage tracking
- Docker image registry

## Contact

For GitLab CI/CD issues, contact the maintainers.
