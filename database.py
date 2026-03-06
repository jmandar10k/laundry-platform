"""
database.py
SQLite database setup for Smart Laundry Operations Platform.
"""

import sqlite3

DB_NAME = "laundry.db"


def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create outlets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outlets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outlet_name TEXT NOT NULL,
            location TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create orders table (with clothing breakdown and delivery_area)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            service_type TEXT NOT NULL,
            service_mode TEXT NOT NULL,
            delivery_area TEXT,
            order_type TEXT DEFAULT 'Delivery',
            shirts INTEGER DEFAULT 0,
            jeans INTEGER DEFAULT 0,
            dresses INTEGER DEFAULT 0,
            traditional INTEGER DEFAULT 0,
            others INTEGER DEFAULT 0,
            items INTEGER NOT NULL,
            outlet_name TEXT NOT NULL,
            status TEXT DEFAULT 'Received',
            batch_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (batch_id) REFERENCES batches(id)
        )
    """)

    # Create notifications table (for automated simulation log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            customer_name TEXT,
            phone TEXT,
            message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)

    # Create batches table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_name TEXT NOT NULL,
            outlet_name TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create drivers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            vehicle_type TEXT,
            vehicle_number TEXT,
            status TEXT DEFAULT 'Available',
            delivery_area TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migration: Add columns if they don't exist (for existing databases)
    cursor.execute("PRAGMA table_info(orders)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if "delivery_area" not in columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN delivery_area TEXT")
    if "order_type" not in columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN order_type TEXT DEFAULT 'Delivery'")
    if "driver_id" not in columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN driver_id INTEGER")

    conn.commit()
    conn.close()


# Auto-initialize on import
init_db()
