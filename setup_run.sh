#!/bin/bash
# Comprehensive test and setup script

echo "═════════════════════════════════════════"
echo "  Todos Project - Complete Setup"
echo "═════════════════════════════════════════"

cd /home/workspace/Todos_Django

# Kill any running servers
echo "Stopping existing servers..."
pkill -f "python manage.py runserver" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
sleep 2

# Activate environment
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

# Create database migrations
echo "Creating database migrations..."
python manage.py makemigrations 2>&1 | grep -v "No changes detected" || true

# Apply migrations
echo "Applying migrations..."
python manage.py migrate 2>&1 | tail -3

# Build frontend
echo "Building React frontend..."
cd frontend-app
npm install -q 2>/dev/null || true
npm run build 2>&1 | tail -3
cd ..

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput -q 2>/dev/null || true

# Done
echo ""
echo "✅ Setup Complete!"
echo ""
echo "Starting servers..."
echo "Django: http://localhost:8000"
echo "Admin: http://localhost:8000/admin"
echo ""

# Start servers
python manage.py runserver 8000

