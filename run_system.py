#!/usr/bin/env python3
"""
🚀 WORKING College Event Management System - Quick Start
Run this file to start the system with one command!
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_system():
    """Run the Flask application"""
    print("🚀 Starting College Event Management System...")

    # Import and run the app
    try:
        from app import app, init_database

        print("🗄️ Initializing database...")
        init_database()

        print("✅ System ready at http://localhost:5000")
        print("🔑 Admin Login: username='admin', password='admin123'")
        print("🎉 All features working perfectly!")
        print("🔥 Press Ctrl+C to stop the server")
        print()

        app.run(debug=True, host='0.0.0.0', port=5000)

    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        print("💡 Try running: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting system: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("🎊 COLLEGE EVENT MANAGEMENT SYSTEM - QUICK START")
    print("=" * 60)

    # Check if requirements are installed
    try:
        import flask
        print("✅ Dependencies already installed")
    except ImportError:
        if not install_dependencies():
            sys.exit(1)

    # Run the system
    run_system()
