from flask import Flask, render_template, request, jsonify
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import our agents
from agents.support_agent import SupportAgent
from db.database_setup import create_database, get_database_path

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize the Support Agent
support_agent = SupportAgent()

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'message': 'Please enter a message.'
            }), 400
        
        # Process the user query through the Support Agent
        response = support_agent.process_user_query(user_message)
        
        return jsonify({
            'success': True,
            'message': response['message'],
            'source': response.get('source', 'unknown'),
            'data': response.get('data')
        })
        
    except Exception as e:
        print(f"Error processing chat request: {e}")
        return jsonify({
            'success': False,
            'message': 'Sorry, I encountered an error while processing your request. Please try again.'
        }), 500

@app.route('/greeting', methods=['GET'])
def get_greeting():
    """Get the initial greeting message"""
    try:
        greeting = support_agent.get_greeting_message()
        sample_queries = support_agent.get_sample_queries()
        
        return jsonify({
            'success': True,
            'greeting': greeting,
            'sample_queries': sample_queries
        })
        
    except Exception as e:
        print(f"Error getting greeting: {e}")
        return jsonify({
            'success': False,
            'greeting': "Hello! I'm your customer support assistant. How can I help you today?",
            'sample_queries': []
        })

@app.route('/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        history = support_agent.get_conversation_history()
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({
            'success': False,
            'history': []
        })

@app.route('/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        support_agent.clear_conversation_history()
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared.'
        })
    except Exception as e:
        print(f"Error clearing history: {e}")
        return jsonify({
            'success': False,
            'message': 'Error clearing history.'
        })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Smart Customer Support Agent',
        'version': '1.0.0'
    })

def initialize_database():
    """Initialize the database if it doesn't exist"""
    db_path = get_database_path()
    if not os.path.exists(db_path):
        print("Database not found. Creating database with sample data...")
        create_database()
        print("Database initialized successfully!")
    else:
        print("Database already exists.")

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("Please create a .env file with your OpenAI API key.")
        print("Copy .env.template to .env and fill in your API key.")
        print("The app will still work for order-related queries without the API key.")
    else:
        print("✅ All environment variables are set.")

if __name__ == '__main__':
    print("🚀 Starting Smart Customer Support Agent...")
    
    # Check environment setup
    check_environment()
    
    # Initialize database
    initialize_database()
    
    # Start the Flask development server
    print("🌐 Starting Flask server...")
    print("📱 Open your browser and go to: http://127.0.0.1:5000")
    print("💬 You can test queries like:")
    print("   - 'Where is my order #1?'")
    print("   - 'What's the status of my earbuds?'")
    print("   - 'Who are you?'")
    print()
    
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )
