#!/bin/bash
#
# Ollama Initialization Script
# This script downloads the required AI models for ShadowScan
#

set -e

echo "🚀 Initializing Ollama for ShadowScan..."
echo ""

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama service to be ready..."
until curl -s http://ollama:11434/api/tags > /dev/null; do
  echo "   Ollama not ready yet, retrying in 5s..."
  sleep 5
done

echo "✅ Ollama is ready!"
echo ""

# Pull Code Analysis Model (Llama 3.1 8B)
echo "📥 Downloading Llama 3.1 8B for code analysis..."
echo "   This may take 5-10 minutes depending on your connection..."
curl -X POST http://ollama:11434/api/pull -d '{
  "name": "llama3.1:8b"
}'

echo ""
echo "✅ Llama 3.1 8B downloaded!"
echo ""

# Pull Vision Model (LLaVA 13B)
echo "📥 Downloading LLaVA 13B for diagram analysis..."
echo "   This is larger and may take 10-20 minutes..."
curl -X POST http://ollama:11434/api/pull -d '{
  "name": "llava:13b"
}'

echo ""
echo "✅ LLaVA 13B downloaded!"
echo ""

# Optional: Pull smaller/alternative models
echo "📥 Downloading additional models (optional)..."

# Codellama for better code analysis
curl -X POST http://ollama:11434/api/pull -d '{
  "name": "codellama:13b"
}'

echo ""
echo "✅ Codellama 13B downloaded!"
echo ""

# List all downloaded models
echo "📋 Currently available models:"
curl -s http://ollama:11434/api/tags | jq '.models[] | .name'

echo ""
echo "🎉 Ollama initialization complete!"
echo ""
echo "ShadowScan is now ready to analyze code and diagrams using local AI models!"
echo "No API keys required! 🚀"
