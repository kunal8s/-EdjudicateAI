#!/bin/bash

# 🚀 EdjudicateAI Deployment Script
# This script helps you prepare and deploy your app to Streamlit Cloud

echo "🧠 EdjudicateAI Deployment Script"
echo "=================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ streamlit_app.py not found. Please run this script from the project root."
    exit 1
fi

echo "📋 Checking prerequisites..."

# Check if requirements_deploy.txt exists
if [ ! -f "requirements_deploy.txt" ]; then
    echo "❌ requirements_deploy.txt not found. Please ensure all deployment files are present."
    exit 1
fi

# Check if .streamlit/config.toml exists
if [ ! -f ".streamlit/config.toml" ]; then
    echo "❌ .streamlit/config.toml not found. Please ensure all deployment files are present."
    exit 1
fi

echo "✅ All deployment files found!"

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy EdjudicateAI to Streamlit Cloud"

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Name it 'EdjudicateAI'"
echo "   - Make it public or private"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "2. Connect your local repository to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/EdjudicateAI.git"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Streamlit Cloud:"
echo "   - Go to https://share.streamlit.io/"
echo "   - Sign in with GitHub"
echo "   - Click 'New app'"
echo "   - Select your repository"
echo "   - Set main file path to: streamlit_app.py"
echo "   - Add your GEMINI_API_KEY in Settings → Secrets"
echo ""
echo "4. Test your deployment!"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "🔑 Don't forget to set your GEMINI_API_KEY in Streamlit Cloud secrets!"
echo ""
echo "Good luck! 🚀"
