#!/bin/bash
# Stop all Wheelchair Robot services

echo "Stopping Wheelchair Robot services..."

if [ -f .service_pids ]; then
    while read pid; do
        if kill -0 $pid 2>/dev/null; then
            echo "Stopping process $pid..."
            kill $pid
        fi
    done < .service_pids
    rm .service_pids
    echo "All services stopped."
else
    echo "No service PIDs file found. Services may not be running."
    echo "Attempting to kill by port..."
    
    # Kill processes by port (fallback)
    lsof -ti:8000 | xargs -r kill
    lsof -ti:8001 | xargs -r kill
    lsof -ti:8002 | xargs -r kill
    lsof -ti:8003 | xargs -r kill
    lsof -ti:8080 | xargs -r kill
    
    echo "Done."
fi
