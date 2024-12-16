#!/bin/bash

SESSION_NAME="blaze-tmux"
ENV_NAME="blazingsql_env"
FLASK_PORT=8889

# Check if the tmux session is running
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session $SESSION_NAME is already running. Terminating it."
  tmux kill-session -t $SESSION_NAME
fi

# Check if the port is in use and kill the process using it
if lsof -i:$FLASK_PORT -t >/dev/null 2>&1; then
  echo "Port $FLASK_PORT is in use. Terminating the process using it."
  fuser -k $FLASK_PORT/tcp
fi

# Start a new tmux session
echo "Starting a new tmux session: $SESSION_NAME"
tmux new-session -d -s $SESSION_NAME

# Send commands to tmux session
tmux send-keys -t $SESSION_NAME "micromamba activate $ENV_NAME" C-m
tmux send-keys -t $SESSION_NAME "flask run --port=$FLASK_PORT" C-m

# Keep the session running in the background
echo "Tmux session $SESSION_NAME started and running in the background."

