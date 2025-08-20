#!/bin/bash

# Render Build Script - Forces pre-built wheels to avoid Rust compilation
echo "🚀 Starting Render build with pre-built wheels..."

# Install dependencies using only pre-built wheels
pip install --only-binary=all -r requirements-render.txt

echo "✅ Build completed successfully!"
