import openai
import os
from typing import Dict, List
from dotenv import load_dotenv
from .logistics_agent import LogisticsAgent

# Load environment variables
load_dotenv()

class SupportAgent:
    """
    Customer Support Agent that serves as the main interface for user interactions.
    It decides whether to handle queries internally or delegate to the Logistics Agent.
    """
    
    def __init__(self):
        # Initialize OpenAI client
        openai.api_key = os.getenv('SECRET_KEY')
        if not openai.api_key:
            print("Warning: SECRET_KEY not found in environment variables")
        
        # Initialize Logistics Agent
        self.logistics_agent = LogisticsAgent()
        
        # Keywords that indicate order-related queries
        self.order_keywords = [
            'order', 'delivery', 'shipping', 'track', 'status', 
            'where', 'when', 'delivered', 'shipped', 'transit',
            'earbuds', 'headphones', 'case', 'cable', 'speaker',
            'package', 'parcel', 'tracking'
        ]
        
        # Cache for conversation context
        self.conversation_history = []
    
    def analyze_intent(self, user_query: str) -> str:
        """
        Analyze user query to determine intent:
        - 'order_related': Queries about orders, delivery, tracking
        - 'general': General questions about company, policies, etc.
        """
        query_lower = user_query.lower()
        
        # Check for order-related keywords
        if any(keyword in query_lower for keyword in self.order_keywords):
            return 'order_related'
        
        # Check for order ID patterns
        import re
        if re.search(r'#?\d+', query_lower):
            return 'order_related'
        
        return 'general'
    
    def handle_general_query(self, user_query: str) -> Dict:
        """
        Handle general queries using OpenAI API with minimal token usage
        """
        response = {
            'success': False,
            'message': '',
            'source': 'openai'
        }
        
        if not openai.api_key:
            response['message'] = "I'm a customer support assistant. For order-related queries, please provide your order number. For general questions, please contact our support team."
            response['success'] = True
            return response
        
        try:
            # System prompt optimized for customer support
            system_prompt = """You are a helpful customer support assistant for an e-commerce company. 
            Keep responses brief (1-2 sentences), friendly, and professional. 
            For order-specific questions, ask for order numbers.
            For general questions, provide helpful information about policies, company info, etc."""
            
            # Initialize OpenAI client
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            
            # Use GPT-3.5-turbo for cost efficiency
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=100,  # Keep it short to save credits
                temperature=0.7
            )
            
            response['success'] = True
            response['message'] = completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback response if API fails
            response['success'] = True
            response['message'] = "I'm here to help! For order tracking, please provide your order number. For other questions, I'll do my best to assist you."
        
        return response
    
    def process_user_query(self, user_query: str) -> Dict:
        """
        Main method to process user queries by determining intent and routing appropriately
        """
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user',
            'message': user_query,
            'timestamp': self._get_timestamp()
        })
        
        # Analyze intent
        intent = self.analyze_intent(user_query)
        
        if intent == 'order_related':
            # Delegate to Logistics Agent
            logistics_response = self.logistics_agent.process_query(user_query)
            
            if logistics_response['success']:
                response = {
                    'message': logistics_response['message'],
                    'success': True,
                    'source': 'logistics_agent',
                    'data': logistics_response.get('data')
                }
            else:
                response = {
                    'message': logistics_response['message'],
                    'success': True,
                    'source': 'logistics_agent'
                }
        else:
            # Handle general queries
            response = self.handle_general_query(user_query)
        
        # Add response to conversation history
        self.conversation_history.append({
            'type': 'assistant',
            'message': response['message'],
            'timestamp': self._get_timestamp(),
            'source': response.get('source', 'unknown')
        })
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Return the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_greeting_message(self) -> str:
        """Return a greeting message for new conversations"""
        return """👋 Hello! I'm your Smart Customer Support Assistant. 

I can help you with:
• Order tracking (e.g., "Where is my order #123?")
• Delivery status updates
• Product inquiries
• General support questions

How can I assist you today?"""
    
    def get_sample_queries(self) -> List[str]:
        """Return sample queries users can try"""
        return [
            "Where is my order #1?",
            "What's the status of my order #2?",
            "When will my earbuds arrive?",
            "Track my delivery",
            "Who are you?",
            "What's your return policy?"
        ]
