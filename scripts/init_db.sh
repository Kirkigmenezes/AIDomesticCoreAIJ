#!/bin/bash
# Database initialization script

set -e

echo "==================================="
echo "Database Initialization Script"
echo "==================================="

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-aiplatform}"
DB_USER="${DB_USER:-aiplatform}"
DB_PASSWORD="${DB_PASSWORD}"

echo "Connecting to database: $DB_HOST:$DB_PORT/$DB_NAME"

# Check if database exists
RESULT=`psql -h $DB_HOST -U $DB_USER -t -c "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" 2>/dev/null`

if [ $RESULT = '1' ]; then
  echo "Database $DB_NAME already exists"
else
  echo "Creating database $DB_NAME..."
  createdb -h $DB_HOST -U $DB_USER $DB_NAME
  echo "Database created successfully"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if needed
echo "Setup complete!"
echo "Database: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"
