#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting Deployment on Oracle Cloud..."

# Load environment variables
source .env

# Build Docker Image
echo "🔨 Building Docker Image..."
docker build -t trading-bot .

# Push Docker Image to Oracle Cloud Registry
echo "📦 Pushing Docker Image to Oracle Cloud Registry..."
docker tag trading-bot your-oracle-repo/trading-bot:latest
docker push your-oracle-repo/trading-bot:latest

# Deploy to Kubernetes
echo "🔄 Applying Kubernetes Deployment..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Verify Deployment
echo "✅ Deployment Successful! Checking Status..."
kubectl get pods -o wide
kubectl get services

echo "🎯 Trading Bot is now live on Oracle Cloud!"

