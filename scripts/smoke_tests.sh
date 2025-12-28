#!/bin/bash
# Smoke tests script

echo "Running Smoke Tests..."
echo "====================="

API_URL="${API_URL:-http://localhost:8000}"

# Test 1: API health check
echo -n "1. API Health Check... "
if curl -s $API_URL/health | grep -q "healthy"; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test 2: Database connectivity
echo -n "2. Database Connectivity... "
if curl -s $API_URL/api/v1/health/db | grep -q "ok"; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test 3: Redis connectivity
echo -n "3. Redis Connectivity... "
if curl -s $API_URL/api/v1/health/cache | grep -q "ok"; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test 4: Quantum module
echo -n "4. Quantum Module... "
RESPONSE=$(curl -s -X POST $API_URL/api/v1/quantum/circuits \
    -H "Authorization: Bearer $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"test","qubits":2}')
if echo $RESPONSE | grep -q "circuit_"; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test 5: Vision module
echo -n "5. Vision Module... "
if curl -s $API_URL/api/v1/vision/health | grep -q "ready"; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test 6: Federated learning
echo -n "6. Federated Learning... "
if curl -s $API_URL/api/v1/federated/health | grep -q "ready"; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

echo ""
echo "All smoke tests passed!"
