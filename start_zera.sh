#!/bin/bash
# 🔒 ZERA - Smart Contract Security Auditor
# Startup script for the Streamlit web interface

echo "🔒 Starting ZERA - Smart Contract Security Auditor"
echo "📊 Web interface powered by Streamlit"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Make sure you're in the correct directory."
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python -c "import streamlit" 2>/dev/null || {
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
}

# Start the Streamlit app
echo "🚀 Starting ZERA web interface..."
echo "🌐 Open your browser to http://localhost:8501"
echo ""

streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
