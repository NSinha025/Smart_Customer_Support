import sqlite3
import os
from datetime import datetime, timedelta

def create_database():
    """Create and populate the SQLite database with sample data"""
    
    # Create db directory if it doesn't exist
    db_dir = os.path.dirname(__file__)
    db_path = os.path.join(db_dir, 'customer_support.db')
    
    # Remove existing database to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_name TEXT NOT NULL,
            delivery_status TEXT NOT NULL,
            expected_date TEXT,
            order_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # Create logistics table
    cursor.execute('''
        CREATE TABLE logistics (
            tracking_id TEXT PRIMARY KEY,
            order_id INTEGER,
            current_location TEXT NOT NULL,
            last_update TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        )
    ''')
    
    # Insert sample customers
    customers_data = [
        (1, 'John Doe', 'john.doe@email.com'),
        (2, 'Jane Smith', 'jane.smith@email.com'),
        (3, 'Mike Johnson', 'mike.johnson@email.com')
    ]
    
    cursor.executemany('INSERT INTO customers (id, name, email) VALUES (?, ?, ?)', customers_data)
    
    # Calculate dates for realistic data
    today = datetime.now()
    order_date1 = (today - timedelta(days=5)).strftime('%Y-%m-%d')
    order_date2 = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    order_date3 = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    
    expected_date1 = (today + timedelta(days=2)).strftime('%Y-%m-%d')
    expected_date2 = (today + timedelta(days=4)).strftime('%Y-%m-%d')
    expected_date3 = (today + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Insert sample orders
    orders_data = [
        (1, 1, 'Wireless Earbuds', 'In Transit', expected_date1, order_date1),
        (2, 2, 'Smartphone Case', 'Processing', expected_date2, order_date2),
        (3, 1, 'USB-C Cable', 'Shipped', expected_date3, order_date3),
        (4, 3, 'Bluetooth Speaker', 'Delivered', (today - timedelta(days=1)).strftime('%Y-%m-%d'), (today - timedelta(days=7)).strftime('%Y-%m-%d'))
    ]
    
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)', orders_data)
    
    # Insert sample logistics data
    logistics_data = [
        ('TRK001', 1, 'Bangalore Hub', (today - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M')),
        ('TRK002', 2, 'Warehouse Delhi', (today - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M')),
        ('TRK003', 3, 'Mumbai Sorting Center', (today - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')),
        ('TRK004', 4, 'Delivered - Customer Location', (today - timedelta(days=1)).strftime('%Y-%m-%d %H:%M'))
    ]
    
    cursor.executemany('INSERT INTO logistics VALUES (?, ?, ?, ?)', logistics_data)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")
    print("Sample data inserted:")
    print("- 3 customers")
    print("- 4 orders")
    print("- 4 logistics entries")

def get_database_path():
    """Return the path to the database"""
    db_dir = os.path.dirname(__file__)
    return os.path.join(db_dir, 'customer_support.db')

if __name__ == "__main__":
    create_database()
