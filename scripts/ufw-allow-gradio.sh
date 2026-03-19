#!/usr/bin/env bash
# Enable traffic to the Gradio web UI port (default: 7860) via UFW.
# Run this on the server (needs sudo privileges).

set -euo pipefail

PORT=${1:-7860}

echo "Allowing TCP port $PORT through UFW..."

sudo ufw allow "$PORT/tcp"

echo "UFW status (filtered):"
sudo ufw status | grep -E "${PORT}(/tcp)?" || true

echo "Done. If UFW was inactive, you may need to run: sudo ufw enable"
