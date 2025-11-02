#!/bin/bash

# Smart Customer Support Agent Setup Script
# This script sets up the entire environment and runs the application

echo "🚀 Smart Customer Support Agent (SCSA) Setup"
echo "============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.template .env
    echo "⚠️  Please edit .env file and add your OpenAI API key (optional for demo)"
else
    echo "✅ .env file already exists"
fi

# Setup database
echo "🗄️  Setting up database..."
python db/database_setup.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Edit .env file to add your OpenAI API key (optional)"
echo "2. Run: python app.py"
echo "3. Open: http://127.0.0.1:5000"
echo ""
echo "Sample queries to test:"
echo "• Where is my order #1?"
echo "• What's the status of my earbuds?"
echo "• Who are you?"
echo ""

# Ask if user wants to start the app now
read -p "Start the application now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Starting Flask application..."
    python app.py
fi
