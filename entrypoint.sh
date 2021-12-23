#!/bin/bash

echo "Setting trap PID $$"
trap cleanup INT TERM

cleanup() {
    echo 'stopping...'
    for APP in $(pgrep 'python' -a |awk '{print $1}'); do
        kill -TERM "$APP"
    done
    wait
    echo "stop"
    exit 0
}

if [ -f /opt/vosk-server/server.py ]; then
    python3 /opt/vosk-server/server.py &
fi

if [ -f /opt/vosk-server/tasks.py ]; then
    python3 /opt/vosk-server/tasks.py &
fi

wait
exit 1
