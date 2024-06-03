#!/usr/bin/env bash
PORT="${PORT:-5050}"
HOST="${HOST:-0.0.0.0}"

# Start the server
uvicorn main:app --host "$HOST" --port "$PORT" --forwarded-allow-ips '*'
