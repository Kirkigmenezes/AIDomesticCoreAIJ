#!/bin/bash
# Advanced development setup and utilities

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Setup development environment
setup_dev_env() {
    log_info "Setting up development environment..."
    
    # Create directories
    mkdir -p logs output data/sample data/test
    
    # Create venv
    if [ ! -d "venv" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install dependencies
    log_info "Installing dependencies..."
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    
    # Setup pre-commit hooks
    log_info "Setting up pre-commit hooks..."
    pre-commit install
    
    log_success "Development environment setup complete!"
}

# Setup database
setup_database() {
    log_info "Setting up database..."
    
    # Check if PostgreSQL is running
    if ! command -v psql &> /dev/null; then
        log_error "PostgreSQL is not installed. Please install PostgreSQL first."
        return 1
    fi
    
    # Create database
    createdb aiplatform 2>/dev/null || log_warning "Database already exists"
    
    # Run migrations
    log_info "Running migrations..."
    alembic upgrade head
    
    # Load sample data
    if [ -f "scripts/load_sample_data.py" ]; then
        log_info "Loading sample data..."
        python scripts/load_sample_data.py
    fi
    
    log_success "Database setup complete!"
}

# Setup Redis
setup_redis() {
    log_info "Setting up Redis..."
    
    if command -v redis-server &> /dev/null; then
        log_info "Starting Redis server..."
        redis-server --daemonize yes
        sleep 1
        
        # Test connection
        if redis-cli ping &> /dev/null; then
            log_success "Redis is running"
        else
            log_error "Redis failed to start"
            return 1
        fi
    else
        log_warning "Redis is not installed. Using Docker..."
        docker run -d -p 6379:6379 --name redis redis:7 2>/dev/null || \
            log_warning "Redis container already running"
    fi
}

# Run tests
run_tests() {
    log_info "Running tests..."
    
    activate_venv
    
    # Unit tests
    log_info "Running unit tests..."
    pytest tests/unit/ -v --cov=aiplatform --cov-report=html
    
    # Integration tests (optional)
    if [ "$1" == "--full" ]; then
        log_info "Running integration tests..."
        pytest tests/integration/ -v
        
        log_info "Running E2E tests..."
        pytest tests/e2e/ -v
    fi
    
    log_success "Tests completed!"
}

# Start development server
start_dev_server() {
    log_info "Starting development server..."
    
    activate_venv
    
    export ENVIRONMENT=development
    export LOG_LEVEL=DEBUG
    
    log_info "Server starting on http://localhost:8000"
    python -m uvicorn aiplatform.main:app --reload --host 0.0.0.0 --port 8000
}

# Start all services (Docker Compose)
start_services() {
    log_info "Starting services with Docker Compose..."
    
    if [ ! -f "docker-compose.yml" ]; then
        log_error "docker-compose.yml not found"
        return 1
    fi
    
    docker-compose up -d
    
    sleep 5
    
    # Check services
    log_info "Checking service health..."
    services=("aiplatform-api" "aiplatform-postgres" "aiplatform-redis" "aiplatform-prometheus")
    
    for service in "${services[@]}"; do
        if docker-compose ps | grep -q "$service"; then
            log_success "$service is running"
        else
            log_error "$service failed to start"
        fi
    done
}

# Stop services
stop_services() {
    log_info "Stopping services..."
    
    if [ -f "docker-compose.yml" ]; then
        docker-compose down
    fi
    
    # Kill local servers if running
    pkill -f "uvicorn" || true
    pkill -f "redis-server" || true
    
    log_success "Services stopped"
}

# Linting and formatting
lint_code() {
    log_info "Running linting..."
    
    activate_venv
    
    log_info "Running flake8..."
    flake8 aiplatform tests --max-line-length=120
    
    log_info "Running mypy..."
    mypy aiplatform --ignore-missing-imports
    
    log_info "Running pylint..."
    pylint aiplatform --disable=R,C
    
    log_success "Linting complete!"
}

format_code() {
    log_info "Formatting code..."
    
    activate_venv
    
    log_info "Running black..."
    black aiplatform tests
    
    log_info "Running isort..."
    isort aiplatform tests
    
    log_success "Formatting complete!"
}

# Build documentation
build_docs() {
    log_info "Building documentation..."
    
    activate_venv
    
    cd docs
    
    if [ -f "Makefile" ]; then
        make clean html
    else
        sphinx-build -b html . _build/html
    fi
    
    cd ..
    
    log_success "Documentation built to docs/_build/html"
}

# Security scan
security_scan() {
    log_info "Running security scan..."
    
    activate_venv
    
    log_info "Running bandit..."
    bandit -r aiplatform -f json -o bandit-report.json
    
    log_info "Running safety check..."
    safety check --json > safety-report.json
    
    log_success "Security scan complete!"
}

# Clean build artifacts
clean() {
    log_info "Cleaning build artifacts..."
    
    rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache .mypy_cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    
    log_success "Cleanup complete!"
}

# Activate virtual environment
activate_venv() {
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        log_error "Virtual environment not found. Run 'setup' first."
        exit 1
    fi
}

# Display help
show_help() {
    cat << EOF
${BLUE}AIDomesticCoreAIJ Development Utility${NC}

Usage: ./dev.sh <command> [options]

Commands:
    setup           Setup development environment
    setup-db        Setup database
    setup-redis     Setup Redis
    tests           Run unit tests (use --full for all tests)
    start           Start development server
    start-all       Start all services with Docker Compose
    stop            Stop all services
    lint            Run linting tools
    format          Format code
    docs            Build documentation
    security        Run security scan
    clean           Clean build artifacts
    help            Show this help message

Examples:
    ./dev.sh setup              # Initial setup
    ./dev.sh start              # Start dev server
    ./dev.sh tests --full       # Run all tests
    ./dev.sh lint && ./dev.sh format

EOF
}

# Main command handler
main() {
    case "${1:-help}" in
        setup)
            setup_dev_env
            setup_database
            setup_redis
            ;;
        setup-db)
            setup_database
            ;;
        setup-redis)
            setup_redis
            ;;
        tests)
            run_tests "$2"
            ;;
        start)
            start_dev_server
            ;;
        start-all)
            start_services
            ;;
        stop)
            stop_services
            ;;
        lint)
            lint_code
            ;;
        format)
            format_code
            ;;
        docs)
            build_docs
            ;;
        security)
            security_scan
            ;;
        clean)
            clean
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
