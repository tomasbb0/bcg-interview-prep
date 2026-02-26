#!/bin/bash
# Deploy cv_platform.html to GitHub Pages (tomasbb0.github.io/cv-platform)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE="$SCRIPT_DIR/cv_platform.html"
DEPLOY_DIR="/tmp/cv-platform-deploy"

if [ ! -f "$SOURCE" ]; then
  echo "❌ cv_platform.html not found at $SOURCE"
  exit 1
fi

# Ensure deploy dir exists with git
if [ ! -d "$DEPLOY_DIR/.git" ]; then
  mkdir -p "$DEPLOY_DIR"
  cd "$DEPLOY_DIR"
  git init
  git remote add origin https://github.com/tomasbb0/cv-platform.git
  git pull origin main
else
  cd "$DEPLOY_DIR"
  git pull origin main 2>/dev/null || true
fi

# Copy and deploy
cp "$SOURCE" "$DEPLOY_DIR/index.html"
cd "$DEPLOY_DIR"
git add index.html
git commit -m "Update CV Platform - $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || { echo "No changes to deploy."; exit 0; }
git push origin main

echo "✅ Deployed to https://tomasbb0.github.io/cv-platform/"
