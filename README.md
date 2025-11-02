# Smart Customer Support Agent (SCSA)

A lightweight, agentic AI system that simulates multi-agent reasoning between a Customer Support Agent and a Logistics Agent.

## 🎯 Overview

This project demonstrates autonomous agent cooperation where:
- **Customer Support Agent** interacts with users and interprets their questions
- **Logistics Agent** handles database lookups and provides order-related information
- Both collaborate to provide clear, accurate responses like a real support team

## ⚙️ Tech Stack

- **Backend**: Python with Flask
- **Database**: SQLite with sample customer and order data  
- **Frontend**: HTML, CSS, JavaScript for chatbot interface
- **AI**: OpenAI GPT-3.5-turbo for natural language understanding
- **Environment**: .env file for secure API key storage

## 🗂️ Project Structure

```
Smart_Customer_Support/
│
├── app.py                     → Flask main file (runs web app)
├── agents/
│   ├── support_agent.py       → Handles user queries and decision-making
│   └── logistics_agent.py     → Fetches order data from the database
├── db/
│   └── database_setup.py      → Creates and populates the database
├── templates/
│   └── index.html             → Chatbot interface page
├── static/
│   └── style.css              → Styling for the chat interface
├── .env.template              → Template for environment variables
├── requirements.txt           → Python dependencies
└── README.md                  → This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Navigate to the project directory
cd Smart_Customer_Support

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the environment template
cp .env.template .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Note**: The system will work for order-related queries even without an OpenAI API key. The AI features are only used for general questions.

### 3. Run the Application

```bash
# Start the Flask server
python app.py
```

The application will:
- Automatically create the SQLite database with sample data
- Start the Flask development server on http://127.0.0.1:5000

### 4. Open Your Browser

Navigate to: **http://127.0.0.1:5000**

## 💬 Testing the System

Try these sample queries to test the multi-agent system:

### Order-Related Queries (Handled by Logistics Agent)
- "Where is my order #1?"
- "What's the status of my order #2?"
- "When will my earbuds arrive?"
- "Track my delivery"

### General Queries (Handled by Support Agent + OpenAI)
- "Who are you?"
- "What's your return policy?"
- "How can I contact support?"

## 🗃️ Database Schema

The system includes sample data with:

**Customers Table**
- John Doe (john.doe@email.com)
- Jane Smith (jane.smith@email.com)  
- Mike Johnson (mike.johnson@email.com)

**Orders Table**
- Order #1: Wireless Earbuds (In Transit)
- Order #2: Smartphone Case (Processing)
- Order #3: USB-C Cable (Shipped)
- Order #4: Bluetooth Speaker (Delivered)

**Logistics Table**
- Real-time tracking information for each order

## 🧠 How It Works

### Multi-Agent Flow

1. **User Query** → Received by Flask app
2. **Support Agent** → Analyzes intent (order-related vs general)
3. **Routing Decision**:
   - Order queries → **Logistics Agent** (database lookup)
   - General queries → **OpenAI API** (AI response)
4. **Response Assembly** → Support Agent formats final response
5. **User Interface** → Displays response in chat

### API Credit Optimization

- Uses GPT-3.5-turbo (cost-effective)
- Limited to 100 tokens per request
- Only calls API for non-order queries
- Caches responses and uses database for order info
- Expected usage: <20 API credits per testing session

## 🎨 Features

- **Real-time Chat Interface**: Modern, responsive design
- **Multi-Agent Coordination**: Demonstrates agent cooperation
- **Sample Query Buttons**: Quick testing of different scenarios
- **Conversation History**: Track chat interactions
- **Status Indicators**: Real-time connection and processing status
- **Mobile Responsive**: Works on all device sizes

## 🔧 Development

### Adding New Features

1. **New Agent**: Create in `agents/` directory
2. **Database Changes**: Modify `db/database_setup.py`
3. **Frontend Updates**: Edit `templates/index.html` and `static/style.css`
4. **API Routes**: Add to `app.py`

### Environment Setup for Development

```bash
# Set Flask environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True

# Run with auto-reload
python app.py
```

## 📈 Possible Enhancements

- Add Knowledge Base Agent for FAQs
- Implement order cancellation/refund workflows
- Email notifications for order status changes
- Support history logging
- Integration with LangChain or LlamaIndex
- Deploy to cloud platforms (Render, Railway)

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated and dependencies installed
2. **Database Not Found**: Run `python db/database_setup.py` manually
3. **API Key Issues**: Check `.env` file exists and contains valid OpenAI key
4. **Port Already in Use**: Change port in `app.py` or kill existing process

### Reset Database

```bash
# Navigate to the db directory
cd db

# Run database setup script
python database_setup.py
```

## 📞 Support

For questions about this demo project:
1. Check the sample queries in the chat interface
2. Review the console logs for error messages
3. Ensure all dependencies are properly installed

## 🎯 Learning Objectives

This project demonstrates:
- Multi-agent AI system architecture
- Database integration with AI agents
- RESTful API design with Flask
- Modern web interface development
- Cost-effective AI API usage patterns
- Real-world customer support workflows

Perfect for learning about AI agent coordination, web development, and practical AI applications!
