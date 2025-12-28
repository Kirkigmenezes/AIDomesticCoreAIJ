#!/bin/bash
# Health check script

set -e

echo "Health Check Script"
echo "==================="

# Check if services are running
echo "Checking services..."

# Check database
echo -n "Database... "
if psql -h ${DB_HOST:-localhost} -U ${DB_USER:-postgres} -d ${DB_NAME:-aiplatform} -c "SELECT 1" &> /dev/null; then
  echo "✓ OK"
else
  echo "✗ FAILED"
  exit 1
fi

# Check Redis
echo -n "Redis... "
if redis-cli -h ${REDIS_HOST:-localhost} ping &> /dev/null; then
  echo "✓ OK"
else
  echo "✗ FAILED"
  exit 1
fi

# Check API
echo -n "API Server... "
if curl -s http://localhost:8000/health > /dev/null; then
  echo "✓ OK"
else
  echo "✗ FAILED"
  exit 1
fi

# Check Prometheus
echo -n "Prometheus... "
if curl -s http://localhost:9090/-/healthy > /dev/null; then
  echo "✓ OK"
else
  echo "✗ FAILED (optional)"
fi

echo ""
echo "Health check completed!"
