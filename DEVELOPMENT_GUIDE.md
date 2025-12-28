# Development Guide - AI Platform SDK

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Testing](#testing)
5. [Code Quality](#code-quality)
6. [Documentation](#documentation)
7. [Git Workflow](#git-workflow)
8. [Debugging](#debugging)

---

## Environment Setup

### Quick Start (Automated)

```bash
# Run setup script
chmod +x setup-dev.sh
./setup-dev.sh

# Or on Windows
python setup-dev.ps1
```

### Manual Setup

```bash
# Clone repository
git clone https://github.com/sorydev/AIDomesticCoreAIJ.git
cd AIDomesticCoreAIJ

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial tests
pytest tests/ -x
```

### Editor Setup

#### VS Code
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python"
  },
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "127"],
  "python.linting.flake8Args": ["--max-line-length=127"]
}
```

#### PyCharm
1. Settings → Project → Python Interpreter → Add Local
2. Select `venv/bin/python`
3. Settings → Editor → Code Style → Python
4. Set line length to 127
5. Enable Black formatter: Tools → Python Integrated Tools → Black

---

## Project Structure

```
aiplatform/
├── __init__.py
├── core.py                 # Core platform
├── mesh_ide.py            # Mesh IDE (Phase 2.4)
├── quantum.py             # Quantum optimization (Phase 2.2)
├── visualization_3d.py    # 3D IDE (Phase 2.3)
├── mesh_ide/              # Mesh IDE submodules
│   ├── __init__.py
│   ├── network.py
│   ├── replication.py
│   └── guardians.py
├── quantum/               # Quantum submodules
├── vision/                # Vision module
├── security/              # Security features
└── [other modules]

tests/
├── __init__.py
├── test_mesh_ide.py
├── test_quantum_code_optimizer.py
├── test_core.py
├── integration_tests.py
└── conftest.py            # pytest configuration

docs/
├── DISTRIBUTED_MESH_IDE_GUIDE.md
├── MESH_IDE_EXAMPLES.md
├── MESH_IDE_INTEGRATION.md
├── QUANTUM_CODE_OPTIMIZATION_GUIDE.md
└── [other documentation]

.github/
├── workflows/
│   ├── tests.yml
│   ├── quality.yml
│   ├── release.yml
│   └── pr.yml
└── ISSUE_TEMPLATE/

.gitlab/
└── [GitLab specific config]

scripts/
├── setup-dev.sh           # Development setup
└── [other utilities]
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
# Update main branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/mesh-ide-optimization
```

### 2. Make Changes

```bash
# Edit files in your editor
# Run tests frequently
pytest tests/test_mesh_ide.py -v

# Format code
black aiplatform/mesh_ide.py
isort aiplatform/mesh_ide.py

# Check quality
flake8 aiplatform/mesh_ide.py
mypy aiplatform/mesh_ide.py
```

### 3. Test Thoroughly

```bash
# Unit tests
pytest tests/test_mesh_ide.py -v

# Integration tests
pytest tests/integration_tests.py -v

# All tests with coverage
pytest tests/ --cov=aiplatform --cov-report=html

# Check coverage report
open htmlcov/index.html
```

### 4. Commit Changes

```bash
# Stage changes
git add aiplatform/mesh_ide.py tests/test_mesh_ide.py

# Commit with conventional format
git commit -m "feat(mesh-ide): add replica optimization

- Optimize replica selection algorithm
- Add load balancing
- Improve performance by 15%

Closes #42"
```

### 5. Push and Create PR

```bash
# Push feature branch
git push origin feature/mesh-ide-optimization

# Create PR on GitHub/GitLab with template
```

---

## Testing

### Test Organization

```python
# tests/test_mesh_ide.py
import pytest
from aiplatform.mesh_ide import MeshIDECoordinator

class TestMeshIDECoordinator:
    """Tests for MeshIDECoordinator."""
    
    @pytest.fixture
    def coordinator(self):
        """Coordinator fixture."""
        return MeshIDECoordinator()
    
    def test_initialization(self, coordinator):
        """Test coordinator initializes."""
        assert coordinator is not None
    
    def test_network_operations(self, coordinator):
        """Test network operations."""
        coordinator.initialize_mesh([
            {'node_id': 'local', 'node_type': 'LOCAL'}
        ])
        assert len(coordinator.network.nodes) == 1
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific file
pytest tests/test_mesh_ide.py

# Run specific test
pytest tests/test_mesh_ide.py::TestMeshIDECoordinator::test_initialization

# Run with coverage
pytest tests/ --cov=aiplatform --cov-report=html

# Run in parallel
pytest tests/ -n auto

# Run with verbose output
pytest tests/ -vv

# Stop on first failure
pytest tests/ -x

# Run slow tests only
pytest tests/ -m slow

# Run excluding slow tests
pytest tests/ -m "not slow"
```

### Testing Best Practices

1. **Use fixtures** for common setup
2. **Mock external dependencies**
3. **Test both success and failure paths**
4. **Aim for >80% coverage**
5. **Use descriptive test names**
6. **Keep tests independent**
7. **Use parametrize for multiple cases**

---

## Code Quality

### Format Code

```bash
# Format with black
black aiplatform tests

# Format imports with isort
isort aiplatform tests

# Combined
black aiplatform tests && isort aiplatform tests
```

### Lint Code

```bash
# flake8
flake8 aiplatform tests --max-line-length=127

# pylint
pylint aiplatform

# Both
make lint
```

### Type Checking

```bash
# mypy
mypy aiplatform --ignore-missing-imports

# strict mode
mypy aiplatform --strict
```

### Security Check

```bash
# bandit
bandit -r aiplatform

# safety
safety check

# pip-audit
pip-audit

# All
make security
```

### Run All Checks

```bash
# Using make
make quality

# Manual
black aiplatform tests
isort aiplatform tests
flake8 aiplatform tests
mypy aiplatform
bandit -r aiplatform
```

### Pre-commit

```bash
# Install hooks
pre-commit install

# Run hooks
pre-commit run --all-files

# Skip hooks temporarily
git commit --no-verify
```

---

## Documentation

### Building Docs

```bash
# Build HTML documentation
cd docs
sphinx-build -b html . _build/html

# Serve locally
python -m http.server 8000 --directory _build/html
# Visit http://localhost:8000
```

### Writing Documentation

```python
def calculate_optimal_route(graph: Dict[str, Dict[str, int]],
                           start: str,
                           end: str) -> int:
    """Calculate shortest path using Dijkstra's algorithm.
    
    Args:
        graph: Adjacency list representation of graph
        start: Starting node ID
        end: Destination node ID
    
    Returns:
        Shortest distance between nodes
    
    Raises:
        ValueError: If start or end node not in graph
        
    Examples:
        >>> graph = {'A': {'B': 1}, 'B': {'A': 1}}
        >>> calculate_optimal_route(graph, 'A', 'B')
        1
    """
```

---

## Git Workflow

### Branch Naming

```
feature/description      New feature
fix/description         Bug fix
docs/description        Documentation
refactor/description    Code refactoring
test/description        Test updates
chore/description       Build, dependencies
```

### Commit Messages

```
feat(scope): short description (< 50 chars)

Longer explanation if needed, wrapped at 72 chars.
Multiple paragraphs are fine.

Closes #123
References #456
```

### Pull Request

1. Base: `develop` (not `main`)
2. Compare: `feature/your-feature`
3. Fill template completely
4. Request reviewers
5. Respond to feedback
6. Squash commits before merge

---

## Debugging

### Using pdb

```python
# Set breakpoint
import pdb; pdb.set_trace()

# Or Python 3.7+
breakpoint()

# In debugger:
# n - next line
# c - continue
# p variable - print variable
# s - step into function
# l - list source
```

### Using ipdb (better debugging)

```bash
pip install ipdb
```

```python
import ipdb; ipdb.set_trace()
```

### Debugging Tests

```bash
# Drop into debugger on failure
pytest tests/ --pdb

# Drop into debugger on first failure
pytest tests/ --pdb -x

# Drop into debugger at start
pytest tests/ --trace
```

### Using logging

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### VS Code Debugging

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal"
        }
    ]
}
```

---

## Useful Commands

```bash
# Make
make help              # Show all commands
make test             # Run tests
make test-cov         # Tests with coverage
make lint             # Run linters
make format           # Format code
make quality          # All quality checks
make docs             # Build documentation
make clean            # Clean generated files

# Git
git status            # Show status
git add <file>        # Stage file
git commit -m "msg"   # Commit
git push              # Push changes
git pull              # Get updates

# Python
python -m pytest      # Run tests
python -m black .     # Format
python -m mypy .      # Type check
```

---

## Getting Help

- **Documentation**: See `/docs` directory
- **Issues**: Check [GitHub Issues](../../issues)
- **Discussions**: See [GitHub Discussions](../../discussions)
- **Code Examples**: See `examples/` and `docs/`

---

Happy coding! 🚀
