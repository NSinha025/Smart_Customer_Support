import sqlite3
import re
import os
from typing import Dict, Optional, List

class LogisticsAgent:
    """
    Logistics Agent handles all database queries related to orders, customers, and shipping.
    This agent is responsible for fetching order status, tracking information, and delivery details.
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to the database in the db directory
            current_dir = os.path.dirname(__file__)
            db_dir = os.path.join(current_dir, '..', 'db')
            self.db_path = os.path.join(db_dir, 'customer_support.db')
        else:
            self.db_path = db_path
    
    def _get_db_connection(self):
        """Create and return a database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # This allows us to access columns by name
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def extract_order_id(self, query: str) -> Optional[int]:
        """Extract order ID from user query using regex"""
        # Look for patterns like "order #123", "order 123", "#123"
        patterns = [
            r'order\s*#?(\d+)',
            r'#(\d+)',
            r'order\s+(\d+)',
            r'id\s*#?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                return int(match.group(1))
        return None
    
    def get_order_info(self, order_id: int) -> Optional[Dict]:
        """Fetch complete order information including customer and logistics data"""
        conn = self._get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            # Join all tables to get complete information
            query = '''
                SELECT 
                    o.order_id,
                    o.product_name,
                    o.delivery_status,
                    o.expected_date,
                    o.order_date,
                    c.name as customer_name,
                    c.email as customer_email,
                    l.tracking_id,
                    l.current_location,
                    l.last_update
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                LEFT JOIN logistics l ON o.order_id = l.order_id
                WHERE o.order_id = ?
            '''
            
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'order_id': result['order_id'],
                    'product_name': result['product_name'],
                    'delivery_status': result['delivery_status'],
                    'expected_date': result['expected_date'],
                    'order_date': result['order_date'],
                    'customer_name': result['customer_name'],
                    'customer_email': result['customer_email'],
                    'tracking_id': result['tracking_id'],
                    'current_location': result['current_location'],
                    'last_update': result['last_update']
                }
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return None
        finally:
            conn.close()
    
    def get_customer_orders(self, customer_email: str = None, customer_name: str = None) -> List[Dict]:
        """Get all orders for a specific customer"""
        conn = self._get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            if customer_email:
                query = '''
                    SELECT 
                        o.order_id,
                        o.product_name,
                        o.delivery_status,
                        o.expected_date,
                        l.current_location
                    FROM orders o
                    LEFT JOIN customers c ON o.customer_id = c.id
                    LEFT JOIN logistics l ON o.order_id = l.order_id
                    WHERE c.email = ?
                    ORDER BY o.order_date DESC
                '''
                cursor.execute(query, (customer_email,))
            elif customer_name:
                query = '''
                    SELECT 
                        o.order_id,
                        o.product_name,
                        o.delivery_status,
                        o.expected_date,
                        l.current_location
                    FROM orders o
                    LEFT JOIN customers c ON o.customer_id = c.id
                    LEFT JOIN logistics l ON o.order_id = l.order_id
                    WHERE c.name LIKE ?
                    ORDER BY o.order_date DESC
                '''
                cursor.execute(query, (f'%{customer_name}%',))
            else:
                return []
            
            results = cursor.fetchall()
            orders = []
            for row in results:
                orders.append({
                    'order_id': row['order_id'],
                    'product_name': row['product_name'],
                    'delivery_status': row['delivery_status'],
                    'expected_date': row['expected_date'],
                    'current_location': row['current_location']
                })
            
            return orders
            
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return []
        finally:
            conn.close()
    
    def search_orders_by_product(self, product_name: str) -> List[Dict]:
        """Search for orders containing a specific product"""
        conn = self._get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = '''
                SELECT 
                    o.order_id,
                    o.product_name,
                    o.delivery_status,
                    o.expected_date,
                    l.current_location,
                    c.name as customer_name
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                LEFT JOIN logistics l ON o.order_id = l.order_id
                WHERE o.product_name LIKE ?
                ORDER BY o.order_date DESC
            '''
            
            cursor.execute(query, (f'%{product_name}%',))
            results = cursor.fetchall()
            
            orders = []
            for row in results:
                orders.append({
                    'order_id': row['order_id'],
                    'product_name': row['product_name'],
                    'delivery_status': row['delivery_status'],
                    'expected_date': row['expected_date'],
                    'current_location': row['current_location'],
                    'customer_name': row['customer_name']
                })
            
            return orders
            
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return []
        finally:
            conn.close()
    
    def process_query(self, user_query: str) -> Dict:
        """
        Main method to process user queries and return relevant order information
        """
        response = {
            'success': False,
            'message': '',
            'data': None
        }
        
        # First try to extract order ID
        order_id = self.extract_order_id(user_query)
        
        if order_id:
            order_info = self.get_order_info(order_id)
            if order_info:
                response['success'] = True
                response['data'] = order_info
                
                # Format a user-friendly message
                status = order_info['delivery_status']
                product = order_info['product_name']
                location = order_info['current_location']
                expected = order_info['expected_date']
                
                if status.lower() == 'delivered':
                    response['message'] = f"Your {product} (Order #{order_id}) has been delivered!"
                elif status.lower() == 'in transit':
                    response['message'] = f"Your {product} (Order #{order_id}) is currently {status.lower()} and located at {location}. Expected delivery: {expected}."
                elif status.lower() == 'shipped':
                    response['message'] = f"Your {product} (Order #{order_id}) has been shipped and is currently at {location}. Expected delivery: {expected}."
                elif status.lower() == 'processing':
                    response['message'] = f"Your {product} (Order #{order_id}) is currently being processed. Expected delivery: {expected}."
                else:
                    response['message'] = f"Your {product} (Order #{order_id}) status: {status}. Expected delivery: {expected}."
            else:
                response['message'] = f"I couldn't find any information for order #{order_id}. Please check the order number and try again."
        
        # Check if query is about a specific product
        elif any(product in user_query.lower() for product in ['earbuds', 'headphones', 'case', 'cable', 'speaker']):
            # Extract product name from query
            product_keywords = {
                'earbuds': 'Earbuds',
                'headphones': 'Headphones', 
                'case': 'Case',
                'cable': 'Cable',
                'speaker': 'Speaker'
            }
            
            for keyword, product_name in product_keywords.items():
                if keyword in user_query.lower():
                    orders = self.search_orders_by_product(product_name)
                    if orders:
                        response['success'] = True
                        response['data'] = orders
                        if len(orders) == 1:
                            order = orders[0]
                            response['message'] = f"Found your {order['product_name']} (Order #{order['order_id']}). Status: {order['delivery_status']}, Expected: {order['expected_date']}."
                        else:
                            response['message'] = f"Found {len(orders)} orders containing '{product_name}'. Here are the details:"
                    else:
                        response['message'] = f"I couldn't find any orders for products containing '{product_name}'."
                    break
        else:
            response['message'] = "I need more specific information to help you. Please provide an order number (e.g., 'Where is my order #123?') or mention a specific product."
        
        return response
