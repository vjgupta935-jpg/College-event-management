#!/bin/bash
echo "========================================"
echo "🚀 College Event Management Setup"
echo "========================================"

echo "📦 Creating virtual environment..."
python3 -m venv venv

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo "🎯 To start the system: python app.py"
echo "🔑 Admin login: admin / admin123"
