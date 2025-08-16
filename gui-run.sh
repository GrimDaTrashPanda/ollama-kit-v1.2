#!/usr/bin/env bash
set -euo pipefail
xhost +local: >/dev/null 2>&1 || true
podman image exists localhost/gramified-gui:v1.2 || { echo "[err] build image first"; exit 1; }
podman run --rm --pull=never \
  --name gramified-gui-v1.2 \
  --userns keep-id \
  --network host \
  -e DISPLAY \
  -e HOME=/tmp \
  -e OLLAMA_HOST=http://127.0.0.1:11434 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v "$(dirname "$0")/bin:/app/bin:ro" \
  --security-opt label=disable \
  localhost/gramified-gui:v1.2
