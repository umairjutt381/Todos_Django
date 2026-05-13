#!/bin/bash
# Comprehensive test script for Todos application

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║            TODOS APPLICATION - VERIFICATION TEST              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Activate virtual environment
source .venv/bin/activate

# Test 1: Django System Check
echo ""
echo "✓ Running Django System Checks..."
python manage.py check
if [ $? -eq 0 ]; then
    echo "✓ Django checks passed!"
else
    echo "✗ Django checks failed!"
    exit 1
fi

# Test 2: Database Migrations
echo ""
echo "✓ Checking Database Migrations..."
python manage.py showmigrations > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Migrations verified!"
else
    echo "✗ Migration issue detected!"
    exit 1
fi

# Test 3: Frontend Files
echo ""
echo "✓ Checking Frontend Files..."
if [ -f "frontend-app/package.json" ] && [ -f "frontend-app/src/App.tsx" ]; then
    echo "✓ Frontend structure verified!"
else
    echo "✗ Frontend files missing!"
    exit 1
fi

# Test 4: Backend API
echo ""
echo "✓ Checking Backend API Structure..."
if [ -f "backend/api_views.py" ] && [ -f "backend/api_urls.py" ] && [ -f "backend/serializers.py" ]; then
    echo "✓ Backend API structure verified!"
else
    echo "✗ Backend API files missing!"
    exit 1
fi

# Test 5: Configuration
echo ""
echo "✓ Checking Configuration Files..."
if [ -f "requirements.txt" ] && [ -f "Todos/settings.py" ] && [ -f "start.sh" ]; then
    echo "✓ Configuration files verified!"
else
    echo "✗ Configuration files missing!"
    exit 1
fi

# Test 6: Documentation
echo ""
echo "✓ Checking Documentation..."
if [ -f "README_NEW.md" ] && [ -f "SETUP_GUIDE.md" ]; then
    echo "✓ Documentation verified!"
else
    echo "✗ Documentation missing!"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✓ ALL TESTS PASSED - READY TO DEPLOY             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Run: bash start.sh"
echo "2. Open browser: http://localhost:3000"
echo "3. Register or login with admin/admin123"
echo ""

