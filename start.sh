#!/bin/bash
# Start the entire Todos application

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    TODOS APPLICATION STARTUP                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}✗ Virtual environment not found${NC}"
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install/Update dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
pip install -q -r requirements.txt

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate

# Start Django server in background
echo -e "${GREEN}✓ Starting Django server on http://localhost:8000${NC}"
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait for Django to start
sleep 2

# Install frontend dependencies
if [ ! -d "frontend-app/node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend-app
    npm install
    cd ..
fi

# Start React development server
echo -e "${GREEN}✓ Starting React server on http://localhost:3000${NC}"
echo -e "${YELLOW}The app will open automatically on the Register page${NC}"
cd frontend-app
npm run dev &
REACT_PID=$!

cd ..

# Function to handle cleanup
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    kill $DJANGO_PID 2>/dev/null
    kill $REACT_PID 2>/dev/null
    echo -e "${GREEN}✓ Shutdown complete${NC}"
}

# Trap signals
trap cleanup EXIT SIGINT SIGTERM

# Keep the script running
echo -e "${GREEN}✓ Both servers are running!${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
wait

