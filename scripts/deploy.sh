#!/bin/bash
# Deployment script for production

set -e

ENV="${1:-production}"
VERSION="${2:-latest}"

echo "=========================================="
echo "Deployment Script"
echo "=========================================="
echo "Environment: $ENV"
echo "Version: $VERSION"

# Load environment variables
if [ -f ".env.$ENV" ]; then
    export $(cat ".env.$ENV" | xargs)
fi

# Build Docker image
echo "Building Docker image..."
docker build -t aiplatform:$VERSION \
    --build-arg VERSION=$VERSION \
    --build-arg ENV=$ENV \
    .

# Tag image
echo "Tagging image..."
docker tag aiplatform:$VERSION gcr.io/project/aiplatform:$VERSION
docker tag aiplatform:$VERSION gcr.io/project/aiplatform:latest

# Push to registry
echo "Pushing to registry..."
docker push gcr.io/project/aiplatform:$VERSION
docker push gcr.io/project/aiplatform:latest

# Deploy with Kubernetes
echo "Deploying to Kubernetes..."
kubectl set image deployment/aiplatform \
    aiplatform=gcr.io/project/aiplatform:$VERSION \
    -n production

# Wait for rollout
echo "Waiting for rollout..."
kubectl rollout status deployment/aiplatform -n production --timeout=5m

# Run smoke tests
echo "Running smoke tests..."
./scripts/smoke_tests.sh

# Notify slack
echo "Sending notification..."
curl -X POST $SLACK_WEBHOOK \
    -H 'Content-Type: application/json' \
    -d "{\"text\": \"Deployment completed: aiplatform $VERSION to $ENV\"}"

echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
