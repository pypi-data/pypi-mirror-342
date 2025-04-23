#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )" # Assumes script is in cyberwave-backend
VENV_PATH="$PROJECT_ROOT/.venv"
SERVER_HOST="0.0.0.0"
SERVER_PORT="8000"
HEALTH_CHECK_URL="http://localhost:$SERVER_PORT/health"
STARTUP_TIMEOUT=10 # Seconds to wait for server startup

# --- Activate Virtual Environment ---
echo "Activating virtual environment at $VENV_PATH..."
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    exit 1
fi
echo "Python executable: $(which python)"
echo "Pytest executable: $(which pytest || echo 'Not found in PATH, using direct path...')"
PYTEST_CMD="$VENV_PATH/bin/pytest"
PYTHON_CMD="$VENV_PATH/bin/python"

# --- Ensure we are in the script's directory ---
cd "$SCRIPT_DIR"

# --- Cleanup function ---
cleanup() {
  echo "Cleaning up..."
  if [ ! -z "$SERVER_PID" ]; then
    echo "Stopping background server (PID: $SERVER_PID)..."
    # Kill the process group to ensure Uvicorn workers are stopped
    # Use pkill to target the process group ID (PGID)
    pkill -SIGTERM -P $SERVER_PID || echo "Server process group already stopped or failed to kill."
    # Fallback kill just in case pkill didn't work or setsid wasn't used
    # kill -SIGTERM -- -$SERVER_PID || echo "Server already stopped."
    wait $SERVER_PID 2>/dev/null # Wait briefly to allow cleanup
  fi
}

# Set trap to run cleanup function on exit or interrupt
trap cleanup EXIT SIGINT SIGTERM

# --- Start Server in Background ---
echo "Starting FastAPI server in background..."
# Use setsid to create a new session, making it easier to kill the whole process group
# setsid "$PYTHON_CMD" -m uvicorn src.main:app --host "$SERVER_HOST" --port "$SERVER_PORT" &
# Simpler backgrounding for broad compatibility:
"$PYTHON_CMD" -m uvicorn src.main:app --host "$SERVER_HOST" --port "$SERVER_PORT" & 
SERVER_PID=$!
echo "Server started with PID: $SERVER_PID"

# --- Wait for Server Startup ---
echo "Waiting for server to become healthy at $HEALTH_CHECK_URL (max ${STARTUP_TIMEOUT}s)..."
SECONDS=0
while true; do
  # Use curl with options: -s (silent), -f (fail fast), -o /dev/null (discard output)
  if curl -sf -o /dev/null "$HEALTH_CHECK_URL"; then
    echo "Server is healthy!"
    break
  fi
  if [ "$SECONDS" -ge "$STARTUP_TIMEOUT" ]; then
    echo "ERROR: Server did not start within $STARTUP_TIMEOUT seconds."
    # Attempt cleanup before exiting
    kill $SERVER_PID || echo "Failed to kill server process $SERVER_PID on startup failure."
    exit 1
  fi
  sleep 1
  SECONDS=$((SECONDS + 1))
done

# --- Run Pytest ---
echo "Running Pytest..."
# Run pytest using the direct path from the venv
"$PYTEST_CMD" "$@" # Pass any arguments from script call to pytest
PYTEST_EXIT_CODE=$?

# --- Exit ---
echo "Tests finished with exit code: $PYTEST_EXIT_CODE"
# Cleanup will be handled by the trap
exit $PYTEST_EXIT_CODE 